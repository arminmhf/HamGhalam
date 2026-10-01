#!/usr/bin/env python3
"""
hamghalam lint — mechanical checks + glossary matching for Persian text.

Usage:
    python3 scripts/lint.py FILE [FILE ...]      # any text/tsx/jsx/html/md/json
    python3 scripts/lint.py -                    # read stdin
    python3 scripts/lint.py --json FILE          # machine-readable

Exit code is always 0; the report is for a human/model to judge, not a gate.
Checks are heuristics. Every hit needs eyes; nothing here is auto-fixable.

All messages below are in English on purpose (cheaper to keep in a model's
context than Persian prose is, token for token); the Persian phrases they
point at — examples, calque pairs, glossary entries — stay Persian, since
those ARE the content being taught, not instructions about it.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TERMS_CORE = os.path.join(HERE, "..", "references", "terms.md")
TERMS_DIR = os.path.join(HERE, "..", "references", "terms")

PERSIAN = "؀-ۿ‌"
PW = f"[{PERSIAN}]"

# ---- mechanical rules -------------------------------------------------------
# (id, severity, regex, message)   severity: E = almost always wrong, W = check
MECH = [
    ("arabic_yeh_kaf", "E", re.compile(r"[يك]"),
     "Arabic «ي/ك»; use Persian «ی/ک»."),
    ("mi_space", "E", re.compile(rf"(?<![{PERSIAN}])ن?می (?={PW})"),
     "«می» with a full space; use a ZWNJ (می‌شود)."),
    ("mi_joined", "W", re.compile(rf"(?<![{PERSIAN}])ن?می(?:شو|کن|تون|توان|ده|گیر|باش|رو|بین|خوا|یاب|رس|ساز|فرست)"),
     "«می» fused to the verb (میشود); use a ZWNJ."),
    ("ha_space", "W", re.compile(rf"{PW}+ ها(?:ی|یی)?(?![{PERSIAN}])"),
     "Plural «ها» with a full space; probably needs a ZWNJ (کتاب‌ها)."),
    ("latin_punct", "W", re.compile(rf"{PW}\s*[,;?]"),
     "Latin punctuation after a Persian word; use «،» «؛» «؟»."),
    ("straight_quotes", "W", re.compile(rf"(?<![=:(,\[{{])(?<![=:(,\[{{] )\"{PW}[^\"\n]{{1,80}}\""),
     "Straight English quotes around Persian text; use «…»."),
    ("latin_digits", "W", re.compile(rf"(?<![A-Za-z0-9_./:=\"'-])(?<![:=] )[0-9]+(?![A-Za-z0-9_./:-])(?=[^\n]*{PW})"),
     "Latin digits in Persian prose; use Persian digits (unless code/ID)."),
    ("tavassot", "E", re.compile(rf"\bتوسط {PW}"),
     "Passive with «توسط»; make the sentence active (pattern 4)."),
    ("nominal", "W", re.compile(r"(اقدام به|انجام (?:دادن|شود|دهید)|مورد \S+ قرار|قابلیت \S+سازی|امکان‌پذیر می‌سازد)"),
     "Nominalization; use a plain verb (pattern 5)."),
    ("allows_you", "E", re.compile(r"(به شما (?:اجازه|امکان) می‌دهد|می‌تواند به شما کمک کند|کمک می‌کند تا)"),
     "Calque of \"allows you to\" / \"helps you\" (pattern 6)."),
    ("not_only", "E", re.compile(r"نه[ ‌]تنها .{2,60}بلکه"),
     "Calque of \"not only … but also\" (pattern 8)."),
    ("intensifier", "W", re.compile(r"(واقعاً|به‌سادگی|به سادگی|به‌راحتی|به راحتی|به‌طور یکپارچه|به طور یکپارچه|به‌طور کامل|به طور کامل|به‌طور مؤثر|بی‌نظیر|در واقع)"),
     "Translated intensifier adverb; probably droppable (pattern 9)."),
    ("comma_before_va", "E", re.compile(r"[،,]\s*(?:و|یا)\s"),
     "Comma before «و»/«یا»; calque of the Oxford comma. Drop the comma or end the sentence with a period (rule 7)."),
    ("imperative_comma_reason", "W", re.compile(r"(?:کنید|ببینید|بروید|بزنید|بگیرید|کن|ببین|برو|بزن)، \S+"),
     "Imperative + comma-attached reason; probably state the result directly (pattern 16) or use a period (pattern 17)."),
    ("parenthetical_adverb", "W", re.compile(r"، (?:حتی|مثلاً|البته|گاهی|همیشه|هر روز|هر شب|نصف‌شب|شب و روز|در صورت نیاز|به‌سرعت)[^،|«\n]{0,25}، "),
     "Parenthetical adverb between two commas; put it at the start or next to the verb (pattern 18)."),
    ("you_just", "E", re.compile(r"(?:^|[.!؟?>]\s*)شما فقط \S+"),
     "Closing \"you just …\" calque (pattern 20)."),
    ("tricolon", "W", re.compile(r"(?:می‌\S+|\S+د)، [^،.\n]{3,60}(?:می‌\S+|\S+د) و [^.\n]{3,80}(?:می‌\S+|\S+د)\."),
     "Three parallel verb clauses; if there's no subject, it's an English advertising tricolon (pattern 19)."),
    ("semicolon", "W", re.compile(r"؛"),
     "Semicolon «؛» only belongs in the formal tone; use a period or «و» elsewhere (rule 6)."),
    ("em_dash", "W", re.compile(r"—"),
     "Em dash as a parenthetical; use a comma or «که» instead (pattern 11)."),
    ("colon_list", "W", re.compile(rf":\s*{PW}[^.\n]*،[^.\n]*(?:،| و ){PW}"),
     "Colon + list; write a full sentence instead (pattern 1)."),
    ("dar_hal_hastid", "W", re.compile(r"در حال \S+ هستید"),
     "\"You are currently …ing\" calque; use a plain sentence (pattern 14)."),
    ("rhetorical_q", "W", re.compile(r"(آیا تا به حال|آماده‌اید\?|آماده‌اید؟|تصور کنید)"),
     "Rhetorical/throat-clearing question (pattern 13)."),
    ("pronoun_khod", "W", re.compile(r"\bشما می‌توانید .{0,40}خود "),
     "«شما … خود»; redundant pronoun (pattern 7)."),
    ("bare_cta", "W", re.compile(r"^(?:\s*)(شروع کنید|بیشتر بدانید|اکنون \S+ کنید)(?:\s*)$"),
     "Bare imperative CTA; a Persian button uses an infinitive/noun (pattern 12)."),
    ("essay_opener", "E", re.compile(r"(در دنیای امروز|در عصر دیجیتال|در این (?:مقاله|متن|پست) به بررسی)"),
     "Clichéd essay-style opening; start directly with a claim or a question (pattern 22)."),
    ("cliche_heading", "W", re.compile(r"^\s*(?:#+\s*)?(چرا باید \S+ را انتخاب کنید|مزایای استفاده از \S+)[؟?]?\s*$"),
     "Clichéd marketing/how-to heading (pattern 23)."),
    ("formal_future", "W", re.compile(r"\S+ خواهد (?:شد|کرد|گرفت|بود)"),
     "Formal future tense «خواهد …»; use the present tense outside a formal register (references/tones.md)."),
]

# pattern 15 calques — keys/values are Persian: the phrase to catch, and the
# fix to suggest, both as actual Persian text.
CALQUES = {
    "خوش برگشتید": "خوش آمدید / حذف",
    "چیزی اشتباه پیش رفت": "مشکلی پیش آمد",
    "ما اینجا هستیم تا کمک کنیم": "اگر مشکلی بود، به ما بگویید",
    "موفقیت!": "انجام شد",
    "چیزی برای نمایش وجود ندارد": "هنوز چیزی ثبت نشده",
    "به جامعهٔ ما بپیوندید": "عضو … شوید",
    "به جامعه ما بپیوندید": "عضو … شوید",
    "در پایان روز": "در نهایت / آخرش",
    "قدرت‌گرفته از": "بر پایهٔ / با فناوری",
    "قدرت گرفته از": "بر پایهٔ / با فناوری",
    "سفر شما": "حذف؛ مستقیم بگو",
    "تجربهٔ کاربری بی‌نظیر": "حذف",
    "هرگونه سؤال": "سؤالی",
    "هرگونه سوال": "سؤالی",
    "به نظر می‌رسد که": "حذف",
    "بدون هیچ‌گونه": "بدون",
    "به سیستم وارد شوید": "وارد شوید",
    "ما معتقدیم که": "حذف؛ مستقیم ادعا را بگو",
    "ما باور داریم که": "حذف؛ مستقیم ادعا را بگو",
}

# document-level heuristics: not line regexes, they look at the whole text
EMOJI_BULLET = re.compile(r"^\s*[\U0001F300-\U0001FAFF☀-➿]\s*\S", re.MULTILINE)
BOLD_SPAN = re.compile(r"\*\*[^*\n]+\*\*")
CLICHE_CLOSING = re.compile(r"^\s*#*\s*(در پایان|جمع‌بندی)[:：]?\s*$", re.MULTILINE)


def lint_document_level(text, fname="-"):
    """Heuristics that only make sense over the whole document, not per line.
    severity 'D' (document): decorative tells that read as AI-generated at a glance."""
    hits = []
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return hits

    emoji_bullets = len(EMOJI_BULLET.findall(text))
    if emoji_bullets >= 3:
        hits.append(dict(file=fname, line=0, sev="D", rule="emoji_bullets",
                         match=f"{emoji_bullets} lines with a leading emoji bullet",
                         msg="Decorative emoji before each bullet; Persian prose uses «-»/«•» or no marker at all."))

    bold_spans = len(BOLD_SPAN.findall(text))
    if bold_spans >= 5 and len(lines) <= 40:
        hits.append(dict(file=fname, line=0, sev="D", rule="bold_overuse",
                         match=f"{bold_spans} bolded spans",
                         msg="Excessive bolding of random phrases; it pulls the reader off the sentence's line of thought."))

    closing = CLICHE_CLOSING.search(text)
    if closing and len(lines) <= 15:
        hits.append(dict(file=fname, line=0, sev="D", rule="cliche_closing",
                         match=closing.group(0).strip(),
                         msg="Clichéd closing heading in a short text; probably unnecessary."))

    return hits

SKIP_LINE = re.compile(r"^\s*(import |export |//|/\*|\*|<\?|#!)")
SKILL_ROOT = os.path.abspath(os.path.join(HERE, ".."))


def load_corpus():
    """Rows from references/terms.md and every file under references/terms/:
    | literal | write | source |. Rows whose fix says "correct, don't change"
    are leave-alone notes and are skipped."""
    rows = []
    paths = [TERMS_CORE]
    if os.path.isdir(TERMS_DIR):
        paths += sorted(
            os.path.join(TERMS_DIR, fn)
            for fn in os.listdir(TERMS_DIR)
            if fn.endswith(".md")
        )
    for path in paths:
        try:
            lines = open(path, encoding="utf-8").read().splitlines()
        except Exception:
            continue
        for line in lines:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 3 or cells[2] not in ("🔵", "🟢") or "correct, don't change" in cells[1]:
                continue
            for phrase in cells[0].split(" / "):
                phrase = re.sub(r"\s*\([^)]*\)", "", phrase)
                phrase = re.sub(r"(?:\s|^)(?:X|…)\.?(?=\s|$)", " ", phrase).strip(" .؟?")
                # single words (خوراک، اشاره، برچسب، جامعه…) are meaning-dependent: too noisy for a linter
                if " " in norm(phrase):
                    rows.append(dict(phrase=phrase, equivalent=cells[1],
                                     source="team" if cells[2] == "🔵" else "community"))
    return rows


def norm(s):
    s = s.replace("‌", " ").replace("ي", "ی").replace("ك", "ک").replace("ٔ", "")
    return re.sub(r"\s+", " ", s)


def lint_text(text, corpus, fname="-"):
    hits = []
    for ln, line in enumerate(text.splitlines(), 1):
        if not re.search(PW, line) or SKIP_LINE.match(line):
            continue
        if "❌" in line:  # deliberate bad example
            continue
        for rid, sev, rx, msg in MECH:
            for m in rx.finditer(line):
                hits.append(dict(file=fname, line=ln, sev=sev, rule=rid,
                                 match=m.group(0).strip(), msg=msg))
        nline = norm(line)
        for calque, fix in CALQUES.items():
            if norm(calque) in nline:
                hits.append(dict(file=fname, line=ln, sev="E", rule="calque",
                                 match=calque, msg=f"Calque; write instead: {fix} (pattern 15)."))
        for e in corpus:
            if norm(e["phrase"]) in nline:
                hits.append(dict(file=fname, line=ln, sev="W", rule="terms",
                                 match=e["phrase"],
                                 msg=f"terms glossary ({e['source']}): try «{e['equivalent']}». Reject if this word means something else here."))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-terms", action="store_true")
    ap.add_argument("--tone", choices=["formal", "semi_formal", "friendly", "casual"], default=None,
                    help="text's tone; with formal, the semicolon warning is silenced")
    a = ap.parse_args()
    corpus = [] if a.no_terms else load_corpus()
    all_hits = []
    for p in a.paths:
        if p != "-" and os.path.abspath(p).startswith(SKILL_ROOT):
            print(f"# {p}: inside the skill itself; ❌ examples and calque tables are deliberately wrong. Skipped.", file=sys.stderr)
            continue
        if p == "-":
            text = sys.stdin.read()
            all_hits += lint_text(text, corpus, "-")
            all_hits += lint_document_level(text, "-")
            continue
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fn in files:
                    if fn.endswith((".md", ".txt", ".tsx", ".jsx", ".ts", ".js", ".html", ".json", ".vue", ".php", ".po", ".yaml", ".yml")):
                        fp = os.path.join(root, fn)
                        try:
                            text = open(fp, encoding="utf-8").read()
                            all_hits += lint_text(text, corpus, fp)
                            all_hits += lint_document_level(text, fp)
                        except UnicodeDecodeError:
                            pass
            continue
        text = open(p, encoding="utf-8").read()
        all_hits += lint_text(text, corpus, p)
        all_hits += lint_document_level(text, p)

    if a.tone == "formal":
        all_hits = [h for h in all_hits if h["rule"] != "semicolon"]
    if a.json:
        print(json.dumps(all_hits, ensure_ascii=False, indent=1))
        return
    if not all_hits:
        print("hamghalam lint: nothing found.")
        return
    order = {"E": 0, "W": 1, "D": 2}
    all_hits.sort(key=lambda h: (order[h["sev"]], h["file"], h["line"]))
    label = {"E": "❌ almost always wrong", "W": "⚠️ check this", "D": "📄 document-level tell"}
    cur = None
    for h in all_hits:
        if h["sev"] != cur:
            cur = h["sev"]
            print(f"\n## {label[cur]}\n")
        loc = h["file"] if h["line"] == 0 else f"{h['file']}:{h['line']}"
        print(f"{loc}  [{h['rule']}]  «{h['match']}»\n    {h['msg']}")
    e = sum(1 for h in all_hits if h["sev"] == "E")
    w = sum(1 for h in all_hits if h["sev"] == "W")
    d = sum(1 for h in all_hits if h["sev"] == "D")
    print(f"\n— {e} error(s), {w} to check, {d} document-level tell(s). None of this is auto-fixed.")


if __name__ == "__main__":
    main()
