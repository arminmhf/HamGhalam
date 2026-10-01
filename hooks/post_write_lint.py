#!/usr/bin/env python3
"""PostToolUse hook for Write/Edit/MultiEdit.

Lints only the Persian text this tool call wrote (Write: content, Edit: new_string,
MultiEdit: every new_string), so untouched lines in a file never come back as
"you wrote this". Hits from rules flagged `hook=True` in lint.py go back to the
model as additionalContext. If the session has Persian copy in it but the
hamghalam skill was never loaded, it also says so once per session: that is how
a button label written in the middle of a coding task reaches the skill.
"""
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "hamghalam", "scripts"))
import lint  # noqa: E402

MAX_HITS = 15
REMIND_AT_WORDS = 12
SKILL_CALL = re.compile(r'"name"\s*:\s*"Skill".*"skill"\s*:\s*"(?:hamghalam:)?hamghalam"')
SKILL_BODY = re.compile(r"Base directory for this skill: [^\"\n]*hamghalam")


def changed_text(tool, ti):
    if tool == "Write":
        return ti.get("content") or ""
    if tool == "Edit":
        return ti.get("new_string") or ""
    if tool == "MultiEdit":
        return "\n".join(e.get("new_string") or "" for e in ti.get("edits") or [])
    return ""


def line_offset(path, text):
    """0-based line where `text` starts in the file now, so reports point at real lines."""
    try:
        body = open(path, encoding="utf-8").read()
    except Exception:
        return 0
    i = body.find(text)
    return body.count("\n", 0, i) if i > 0 else 0


def skill_loaded(transcript):
    try:
        with open(transcript, encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "hamghalam" in line and (SKILL_CALL.search(line) or SKILL_BODY.search(line)):
                    return True
    except Exception:
        pass
    return False


def remind_once(session):
    flag = os.path.join(tempfile.gettempdir(), f"hamghalam-reminded-{re.sub(r'[^A-Za-z0-9_-]', '', session or 'x')}")
    if os.path.exists(flag):
        return False
    try:
        open(flag, "w").close()
    except Exception:
        pass
    return True


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ""
    text = changed_text(tool, ti)
    if not path or not re.search(lint.PW, text):
        return
    if os.path.abspath(path).startswith(ROOT + os.sep):
        return  # the plugin's own files are full of deliberate bad examples

    words = len(re.findall(rf"{lint.PW}+", text))
    offset = 0 if tool == "Write" else line_offset(path, text)
    hits = lint.lint_text(text, lint.load_corpus(), path, offset)
    if tool == "Write" or text.count("\n") >= 8:
        hits += lint.lint_document_level(text, path)
    hits = [h for h in hits if h.get("hook")]

    parts = []
    if hits:
        order = {"E": 0, "D": 1, "W": 2}
        hits.sort(key=lambda h: (order[h["sev"]], h["line"]))
        rows = []
        for h in hits[:MAX_HITS]:
            loc = path if h["line"] == 0 else f"{path}:{h['line']}"
            rows.append(f"- {loc} [{h['rule']}] «{h['match']}»: {h['msg']}")
        more = f"\n(و {len(hits) - MAX_HITS} مورد دیگر؛ لینتر را روی فایل اجرا کن.)" if len(hits) > MAX_HITS else ""
        parts.append("hamghalam: در متن فارسی‌ای که همین حالا نوشتی این نشانه‌ها پیدا شد:\n"
                     + "\n".join(rows) + more
                     + "\nهر مورد را بسنج. اگر عمدی است (مثال عمداً نادرست، نقل‌قول، متن کاربر) رد شو، وگرنه همین حالا اصلاحش کن.")
    if words >= REMIND_AT_WORDS and not skill_loaded(data.get("transcript_path", "")) and remind_once(data.get("session_id")):
        parts.append("hamghalam: این تسک متن فارسی تولید می‌کند ولی اسکیل هم‌قلم در این جلسه بارگذاری نشده است. "
                     "پیش از نوشتن یا اصلاح متن فارسی بیشتر، اسکیل hamghalam را با ابزار Skill فراخوانی کن و طبق آن بنویس.")
    if not parts:
        return
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                             "additionalContext": "\n\n".join(parts)}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
