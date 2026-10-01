#!/usr/bin/env bash
# PostToolUse hook: after Write/Edit, runs hamghalam's lint.py on the touched
# file and feeds the result back automatically, so Persian strings written as
# a side effect of unrelated tasks (a button label inside a React component,
# an error message) don't skip review just because nobody said "با هم‌قلم".
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINT="$HERE/../scripts/lint.py"

input="$(cat)"
file_path="$(python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get("tool_input", {}).get("file_path", ""))
except Exception:
    print("")
' <<<"$input")"

if [[ -z "$file_path" || ! -f "$file_path" ]]; then
    exit 0
fi

report="$(python3 "$LINT" --json "$file_path" 2>/dev/null || true)"
if [[ -z "$report" || "$report" == "[]" ]]; then
    exit 0
fi

errors="$(python3 -c '
import json, sys
hits = json.loads(sys.argv[1])
for h in hits:
    if h.get("sev") != "E":
        continue
    line = "{}:{}  [{}]  «{}»  —  {}".format(h["file"], h["line"], h["rule"], h["match"], h["msg"])
    print(line)
' "$report" 2>/dev/null || true)"

if [[ -z "$errors" ]]; then
    exit 0
fi

{
    echo "hamghalam: the Persian string(s) you just wrote have translation tells (even if the task wasn't about writing copy):"
    echo "$errors"
    echo "If this is unintentional, fix it now; if it's deliberate (e.g. a subjectless passive, or a deliberately bad example), reject it."
} >&2

exit 2
