#!/bin/sh
# Install the landing-page-system skill for one or more coding agents.
#
#   ./install.sh [--agent all|claude|codex|agents|pi|opencode|gemini|cursor] [--link|--copy]
#                [--bin-dir DIR] [--force] [--uninstall]
#
# Default: symlink into ~/.agents/skills/ and into the skills folder of every agent whose home
# folder exists on this machine, then symlink bin/lp into ~/.local/bin if that is on PATH.
# Idempotent. Never replaces a real (non-symlink) folder or file without --force.

set -eu

NAME=landing-page-system
SRC=$(cd -P "$(dirname "$0")" && pwd)
AGENT=""
MODE=link
BIN_DIR=""
BIN_EXPLICIT=0
FORCE=0
UNINSTALL=0
MARKER=.lp-installed

usage() {
  sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
}

while [ $# -gt 0 ]; do
  case $1 in
    --agent) [ $# -ge 2 ] || { usage; exit 2; }; AGENT=$2; shift 2 ;;
    --agent=*) AGENT=${1#--agent=}; shift ;;
    --link) MODE=link; shift ;;
    --copy) MODE=copy; shift ;;
    --bin-dir) [ $# -ge 2 ] || { usage; exit 2; }; BIN_DIR=$2; BIN_EXPLICIT=1; shift 2 ;;
    --bin-dir=*) BIN_DIR=${1#--bin-dir=}; BIN_EXPLICIT=1; shift ;;
    --force) FORCE=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "install.sh: unknown option $1" >&2; usage >&2; exit 2 ;;
  esac
done

# agent -> "home folder|skills folder"
agent_dirs() {
  case $1 in
    agents) echo "$HOME/.agents|$HOME/.agents/skills" ;;
    claude) echo "$HOME/.claude|$HOME/.claude/skills" ;;
    codex) echo "$HOME/.codex|$HOME/.codex/skills" ;;
    pi) echo "$HOME/.pi|$HOME/.pi/agent/skills" ;;
    opencode) echo "$HOME/.config/opencode|$HOME/.config/opencode/skills" ;;
    gemini) echo "$HOME/.gemini|$HOME/.gemini/skills" ;;
    cursor) echo "$HOME/.cursor|$HOME/.cursor/skills" ;;
    *) return 1 ;;
  esac
}
ALL="agents claude codex pi opencode gemini cursor"

case $AGENT in
  "") TARGETS=agents
      for a in claude codex pi opencode gemini cursor; do
        home=$(agent_dirs "$a" | cut -d'|' -f1)
        [ -d "$home" ] && TARGETS="$TARGETS $a"
      done ;;
  all) TARGETS=$ALL ;;
  *) agent_dirs "$AGENT" >/dev/null || { echo "install.sh: unknown agent '$AGENT' (use: all $ALL)" >&2; exit 2; }
     TARGETS=$AGENT ;;
esac

[ -n "$BIN_DIR" ] || BIN_DIR=$HOME/.local/bin

on_path() {
  case ":$PATH:" in *":$1:"*) return 0 ;; *) return 1 ;; esac
}

copy_skill() {
  mkdir -p "$1"
  for item in SKILL.md README.md LICENSE CHANGELOG.md install.sh bin scripts references templates; do
    [ -e "$SRC/$item" ] && cp -R "$SRC/$item" "$1/"
  done
  : > "$1/$MARKER"
}

remove_ok() {  # may we replace or remove this path?
  [ -L "$1" ] || [ -f "$1/$MARKER" ] || [ "$FORCE" = 1 ]
}

FIRST=""
for a in $TARGETS; do
  dir=$(agent_dirs "$a" | cut -d'|' -f2)
  dest=$dir/$NAME
  if [ "$UNINSTALL" = 1 ]; then
    if [ ! -e "$dest" ] && [ ! -L "$dest" ]; then
      echo "skip     $dest (not installed)"
    elif remove_ok "$dest"; then
      rm -rf "$dest"
      echo "removed  $dest"
    else
      echo "kept     $dest (a folder this script did not create; use --force to remove it)"
    fi
    continue
  fi
  if [ -L "$dest" ] && [ "$MODE" = link ] && [ "$(cd -P "$dest" 2>/dev/null && pwd)" = "$SRC" ]; then
    echo "ok       $dest -> $SRC (already linked)"
  elif [ -e "$dest" ] || [ -L "$dest" ]; then
    if remove_ok "$dest"; then
      rm -rf "$dest"
      mkdir -p "$dir"
      if [ "$MODE" = link ]; then ln -s "$SRC" "$dest"; else copy_skill "$dest"; fi
      echo "updated  $dest ($MODE)"
    else
      echo "kept     $dest (a real folder is in the way; use --force to replace it)"
      continue
    fi
  else
    mkdir -p "$dir"
    if [ "$MODE" = link ]; then ln -s "$SRC" "$dest"; else copy_skill "$dest"; fi
    echo "$( [ "$MODE" = link ] && echo linked || echo copied )   $dest"
  fi
  [ -n "$FIRST" ] || FIRST=$dest
done

# The lp command on PATH.
lp_link=$BIN_DIR/lp
if [ "$UNINSTALL" = 1 ]; then
  if [ -L "$lp_link" ]; then
    rm -f "$lp_link"
    echo "removed  $lp_link"
  fi
  exit 0
fi
if [ -z "$FIRST" ]; then
  echo "No skill folder installed, so lp was not linked."
  exit 1
fi
if [ "$BIN_EXPLICIT" = 0 ] && ! on_path "$BIN_DIR"; then
  echo "skip     $lp_link ($BIN_DIR is not on PATH; rerun with --bin-dir DIR, or use $FIRST/bin/lp)"
elif [ -e "$lp_link" ] && [ ! -L "$lp_link" ] && [ "$FORCE" = 0 ]; then
  echo "kept     $lp_link (a real file is in the way; use --force to replace it)"
else
  mkdir -p "$BIN_DIR"
  ln -sfn "$FIRST/bin/lp" "$lp_link"
  echo "linked   $lp_link -> $FIRST/bin/lp"
fi
echo "Done. Try: lp --help   (inside a project: lp init \"<product>\")"
