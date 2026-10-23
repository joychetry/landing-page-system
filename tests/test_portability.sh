#!/usr/bin/env bash
# Portability test: install the skill into fake HOMEs for several agents, run lp through the
# wrapper with a scrubbed environment (env -i), then run a workspace's vendored .lp/lp.py with
# the skill uninstalled. Also exercises install.sh (link, idempotent rerun, copy, uninstall).
#
#   bash tests/test_portability.sh

set -euo pipefail

ROOT=$(cd -P "$(dirname "$0")/.." && pwd)
PY=$(command -v python3)
CLEAN_PATH="$(dirname "$PY"):/usr/bin:/bin"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/lp-port.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
PASS=0
FAIL=0

ok() { PASS=$((PASS + 1)); echo "ok    $*"; }
bad() { FAIL=$((FAIL + 1)); echo "FAIL  $*"; }
check() {  # check "description" command...
  local desc=$1; shift
  if "$@" >"$TMP/out" 2>&1; then ok "$desc"; else bad "$desc"; sed 's/^/      /' "$TMP/out"; fi
}
is_json() { "$PY" -c 'import json, sys; json.load(sys.stdin)'; }

# Run with a scrubbed environment: only HOME and a minimal PATH.
clean() {  # clean HOME CWD command...
  local home=$1 cwd=$2; shift 2
  (cd "$cwd" && env -i HOME="$home" PATH="$CLEAN_PATH" "$@")
}

install_copy() {  # copy the shipped skill files into a skills dir
  mkdir -p "$1"
  for item in SKILL.md README.md LICENSE CHANGELOG.md install.sh bin scripts references templates; do
    cp -R "$ROOT/$item" "$1/"
  done
}

for layout in .agents/skills .claude/skills .codex/skills .pi/agent/skills .config/opencode/skills; do
  H=$TMP/home-$(echo "$layout" | tr '/.' '__')
  SK=$H/$layout/landing-page-system
  mkdir -p "$H/work" "$H/bin"
  install_copy "$SK"
  # A copy of the wrapper outside the skill: forces lookup through the conventional dirs.
  cp "$ROOT/bin/lp" "$H/bin/lp"

  for wrapper in "$SK/bin/lp" "$H/bin/lp"; do
    tag="$layout via ${wrapper#$H/}"
    check "$tag: lp --help" clean "$H" "$H/work" sh "$wrapper" --help
    check "$tag: lp --version" sh -c "env -i HOME='$H' PATH='$CLEAN_PATH' sh '$wrapper' --version | grep -q 1.1.0"
  done
  check "$layout: lp init" clean "$H" "$H/work" sh "$H/bin/lp" init "Port Test"
  check "$layout: workspace has vendored .lp/lp.py" test -f "$H/work/port-test/.lp/lp.py"
  check "$layout: lp next --json parses" sh -c "cd '$H/work/port-test' && env -i HOME='$H' PATH='$CLEAN_PATH' \
    sh '$H/bin/lp' next --json | '$PY' -c 'import json,sys; d=json.load(sys.stdin); assert d[\"step\"] == 1'"
  check "$layout: lp next from a subfolder" sh -c "cd '$H/work/port-test/research' && env -i HOME='$H' \
    PATH='$CLEAN_PATH' sh '$H/bin/lp' next --json | '$PY' -c 'import json,sys; json.load(sys.stdin)'"

  # Uninstall the skill: the workspace must keep working on its own.
  rm -rf "$SK"
  check "$layout: vendored lp.py runs with the skill uninstalled" sh -c "cd '$H/work/port-test' && \
    env -i HOME='$H' PATH='$CLEAN_PATH' '$PY' .lp/lp.py next --json | '$PY' -c 'import json,sys; json.load(sys.stdin)'"
  check "$layout: wrapper falls back to the vendored .lp/lp.py" sh -c "cd '$H/work/port-test/pages' && \
    env -i HOME='$H' PATH='$CLEAN_PATH' sh '$H/bin/lp' status --json | '$PY' -c 'import json,sys; json.load(sys.stdin)'"
  check "$layout: vendored start works" clean "$H" "$H/work/port-test" "$PY" .lp/lp.py start 1
  check "$layout: template copied by vendored start" test -f "$H/work/port-test/research/01-goal-offer.md"
  # Moved workspace still works.
  mv "$H/work/port-test" "$H/moved"
  check "$layout: moved workspace still runs" clean "$H" "$H/moved" "$PY" .lp/lp.py status
  # Nothing to find at all: exit 127 with a clear message.
  set +e
  out=$(cd "$H" && env -i HOME="$H" PATH="$CLEAN_PATH" sh "$H/bin/lp" --help 2>&1)
  code=$?
  set -e
  if [ "$code" = 127 ] && printf '%s' "$out" | grep -q "cannot find lp.py"; then
    ok "$layout: wrapper exits 127 when nothing is installed"
  else
    bad "$layout: wrapper exits 127 when nothing is installed (got $code: $out)"
  fi
done

# LP_SKILL_HOME resolution.
H=$TMP/home-env
mkdir -p "$H/bin" "$H/work"
cp "$ROOT/bin/lp" "$H/bin/lp"
check "LP_SKILL_HOME: wrapper uses it" sh -c "cd '$H/work' && env -i HOME='$H' PATH='$CLEAN_PATH' \
  LP_SKILL_HOME='$ROOT' sh '$H/bin/lp' --version | grep -q 1.1.0"

# Wrapper reached through a symlink (how install.sh puts it on PATH).
mkdir -p "$TMP/linkbin"
ln -s "$ROOT/bin/lp" "$TMP/linkbin/lp"
check "symlinked wrapper resolves its real location" sh -c "cd '$TMP' && env -i HOME='$TMP/nohome' \
  PATH='$TMP/linkbin:$CLEAN_PATH' lp --version | grep -q 1.1.0"

# install.sh in a fake HOME.
H=$TMP/home-install
mkdir -p "$H/.claude" "$H/.codex" "$H/.local/bin"
inst() { env -i HOME="$H" PATH="$H/.local/bin:$CLEAN_PATH" sh "$ROOT/install.sh" "$@"; }
check "install.sh default (link)" inst
check "install.sh linked ~/.agents" test -L "$H/.agents/skills/landing-page-system"
check "install.sh linked existing ~/.claude" test -L "$H/.claude/skills/landing-page-system"
check "install.sh linked existing ~/.codex" test -L "$H/.codex/skills/landing-page-system"
check "install.sh skipped missing ~/.gemini" test ! -e "$H/.gemini"
check "install.sh linked lp on PATH" test -L "$H/.local/bin/lp"
check "installed lp runs" sh -c "env -i HOME='$H' PATH='$H/.local/bin:$CLEAN_PATH' lp --version | grep -q 1.1.0"
check "install.sh is idempotent" sh -c "env -i HOME='$H' PATH='$H/.local/bin:$CLEAN_PATH' sh '$ROOT/install.sh' \
  | grep -q 'already linked'"
mkdir -p "$H/.gemini/skills/landing-page-system"
check "install.sh never clobbers a real folder" sh -c "env -i HOME='$H' PATH='$CLEAN_PATH' sh '$ROOT/install.sh' \
  --agent gemini | grep -q kept"
check "install.sh --copy --agent pi" inst --agent pi --copy
check "copied skill has scripts/lp.py" test -f "$H/.pi/agent/skills/landing-page-system/scripts/lp.py"
check "install.sh --copy rerun is idempotent" inst --agent pi --copy
check "install.sh --uninstall" inst --uninstall
check "uninstall removed links" test ! -e "$H/.agents/skills/landing-page-system" -a ! -e "$H/.local/bin/lp"
check "uninstall kept the real folder" test -d "$H/.gemini/skills/landing-page-system"
check "install.sh --uninstall --agent pi removes its copy" sh -c "env -i HOME='$H' PATH='$CLEAN_PATH' \
  sh '$ROOT/install.sh' --agent pi --uninstall && test ! -e '$H/.pi/agent/skills/landing-page-system'"
check "install.sh rejects unknown agents" sh -c "! env -i HOME='$H' PATH='$CLEAN_PATH' sh '$ROOT/install.sh' --agent nope"

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" = 0 ]
