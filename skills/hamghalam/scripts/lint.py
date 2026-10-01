#!/usr/bin/env python3
"""
hamghalam lint — mechanical checks + translationese heuristics for Persian text.

Usage:
    python3 scripts/lint.py FILE [FILE ...]      # any text/tsx/jsx/html/md/json
    python3 scripts/lint.py -                    # read stdin
    python3 scripts/lint.py --json FILE          # machine-readable
    python3 scripts/lint.py --tone formal FILE   # tone-dependent rules adjust

Exit code is always 0; the report is for a human/model to judge, not a gate.
Messages are in English; the Persian phrases they point at stay Persian.
Checks are heuristics. Every hit needs eyes; nothing here is auto-fixable.

Severity:
    E  almost always wrong
    W  check it; often wrong, sometimes fine
    D  document-level decoration that reads as machine-written
The `hook` flag marks rules the PostToolUse hook reports back to the model
(every E rule, plus the W rules that point at sentence architecture rather
than style preference).
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TERMS_CORE = os.path.join(HERE, "..", "references", "terms.md")
TERMS_DIR = os.path.join(HERE, "..", "references", "terms")
SOURCES = {"🔵": "team-edited", "🟢": "community", "✍️": "copywriter"}

PERSIAN = "؀-ۿ‌"
PW = f"[{PERSIAN}]"
NB = f"(?<![{PERSIAN}])"   # not preceded by a Persian letter (word start)
NA = f"(?![{PERSIAN}])"    # not followed by a Persian letter (word end)
SENT = r"(?:^|[.!؟?»:]\s*|\n)"  # sentence start

# (id, severity, hook, regex, message)
MECH = [
    # ---- mechanical ----
    ("arabic_yeh_kaf", "E", True, re.compile(r"[يك]"),
     "Arabic «ي/ك»; use Persian «ی/ک»."),
    ("mi_space", "E", True, re.compile(rf"{NB}ن?می (?={PW})"),
     "«می» with a full space; use a ZWNJ (می‌شود)."),
    ("mi_joined", "W", True, re.compile(rf"{NB}ن?می(?:شو|کن|تون|توان|ده|گیر|باش|رو|بین|خوا|یاب|رس|ساز|فرست)"),
     "«می» fused to the verb (میشود); use a ZWNJ."),
    ("ha_space", "W", False, re.compile(rf"{PW}+ ها(?:ی|یی)?{NA}"),
     "Plural «ها» with a full space; probably needs a ZWNJ (کتاب‌ها)."),
    ("latin_punct", "W", False, re.compile(rf"{PW}\s*[,;?]"),
     "Latin punctuation after a Persian word; use «،» «؛» «؟»."),
    ("straight_quotes", "W", False, re.compile(rf"(?<![=:(,\[{{])(?<![=:(,\[{{] )\"{PW}[^\"\n]{{1,80}}\""),
     "Straight English quotes around Persian text; use «…»."),
    ("latin_digits", "W", False, re.compile(rf"(?<![A-Za-z0-9_./:=\"'-])(?<![:=] )[0-9]+(?![A-Za-z0-9_./:-])(?=[^\n]*{PW})"),
     "Latin digits in Persian prose; use Persian digits (unless code/ID)."),
    ("slash_247", "E", True, re.compile(r"(?:۲۴|24)\s*/\s*(?:۷|7)"),
     "«۲۴/۷» is a calque of 24/7; write «شبانه‌روزی» (patterns C2)."),

    # ---- sentence architecture ----
    ("tavassot", "E", True, re.compile(rf"{NB}توسط {PW}"),
     "Passive with «توسط»; make the sentence active (patterns B5)."),
    ("nominal", "W", True, re.compile(r"(اقدام به|انجام (?:دادن|شود|دهید)|مورد \S+ قرار|قابلیت \S+سازی|امکان‌پذیر می‌سازد)"),
     "Nominalization; use a plain verb (patterns B6)."),
    ("allows_you", "E", True, re.compile(r"(به شما (?:اجازه|امکان) می‌دهد|می‌تواند به شما کمک کند|کمک می‌کند تا)"),
     "Calque of \"allows you to\" / \"helps you\" (patterns B7)."),
    ("not_only", "E", True, re.compile(r"نه[ ‌]تنها .{2,60}بلکه"),
     "Calque of \"not only … but also\" (patterns B9)."),
    ("not_just", "E", True, re.compile(r"فقط یک [^.،؛\n]{1,40} نیست"),
     "Calque of \"it's not just X, it's Y\"; say what it is (patterns B9)."),
    ("lets", "E", True, re.compile(rf"{NB}بیایید{NA}"),
     "«بیایید…» is a calque of \"Let's\" (patterns C2)."),
    ("cleft", "W", True, re.compile(r"این (?:شما|ما|او|آن‌ها|شمایید) (?:هستید|هستیم|است|هستند) که"),
     "Cleft «این … است که» (\"It's you who …\"); say it plainly (patterns B10)."),
    ("this_is_where", "E", True, re.compile(r"(?:اینجا|این‌جا)ست که"),
     "Calque of \"This is where … comes in\" (patterns B12)."),
    ("this_means", "W", True, re.compile(rf"{SENT}این یعنی"),
     "Sentence opening with «این یعنی» (\"This means\"); put the result in the sentence itself (patterns B12)."),
    ("indef_yek", "W", True, re.compile(rf"{NB}یک {PW}+(?: {PW}+)? (?:است|هستیم|هستید|هستند){NA}"),
     "English-style indefinite «یک» (a/an); «…ی است» is usually more natural (دستیار هوشمندی است) (patterns B4)."),
    ("we_are_a", "W", True, re.compile(rf"{SENT}ما یک [^.\n]{{1,50}} هستیم"),
     "«ما یک … هستیم» (\"We are a …\"); open with the work itself (patterns A5)."),
    ("with_using", "W", True, re.compile(rf"{SENT}با استفاده از"),
     "Sentence opening with «با استفاده از» (\"Using …\"); «با X» is usually enough (patterns B13)."),
    ("discourse_marker", "W", True, re.compile(rf"{SENT}(همچنین|علاوه بر این|به عبارت دیگر|در نتیجه|در واقع)،"),
     "English-style discourse marker opening the sentence (Moreover/Additionally); join it to the previous sentence or drop the marker (patterns B11)."),
    ("intensifier", "W", False, re.compile(r"(واقعاً|به‌سادگی|به سادگی|به‌راحتی|به راحتی|به‌طور یکپارچه|به طور یکپارچه|به‌طور کامل|به طور کامل|به‌طور مؤثر|بی‌نظیر|در واقع)"),
     "Translated intensifier; probably droppable (patterns C1)."),
    ("comma_before_va", "W", True, re.compile(r"[،,]\s*(?:و|یا)\s"),
     "Comma before «و»/«یا»; in a list it's the Oxford comma calque (mechanics 7)."),
    ("imperative_comma_reason", "W", False, re.compile(rf"{NB}(?:کنید|ببینید|بروید|بزنید|بگیرید|کن|ببین|برو|بزن)، \S+"),
     "Imperative + comma-attached reason; stating the result directly may read more naturally."),
    ("parenthetical_adverb", "W", True, re.compile(r"، (?:حتی|مثلاً|البته|گاهی|همیشه|هر روز|هر شب|نصف‌شب|نیمه‌شب|شب و روز|در صورت نیاز|به‌سرعت)[^،|«\n]{0,25}، "),
     "Adverb wedged between two commas; put it at the start or next to the verb (patterns B16)."),
    ("you_just", "E", True, re.compile(r"(?:^|[.!؟?>]\s*|\sو\s)شما فقط \S+"),
     "Closing \"you just …\" punchline (patterns A2)."),
    ("punchline_only", "W", True, re.compile(r"(?:سهم|کار) شما فقط"),
     "The same closing punchline in other words; the device itself is English, not the wording (patterns A2)."),
    ("tricolon", "W", True, re.compile(r"(?:می‌\S+|\S+د)، [^،.\n]{3,60}(?:می‌\S+|\S+د) و [^.\n]{3,80}(?:می‌\S+|\S+د)\."),
     "Three parallel subjectless verb clauses; English ad-copy tricolon (patterns A3)."),
    ("semicolon", "W", False, re.compile(r"؛"),
     "«؛» is rare in web copy; one in every paragraph reads as machine-written (mechanics 6)."),
    ("em_dash", "W", True, re.compile(r"—"),
     "Em dash as a parenthetical; use a comma or «که» (patterns B15)."),
    ("colon_list", "W", True, re.compile(rf":\s*{PW}[^.\n]*،[^.\n]*(?:،| و ){PW}"),
     "Colon + list; write a full sentence (patterns B3)."),
    ("dar_hal_hastid", "W", True, re.compile(r"در حال \S+ هستید"),
     "\"You are currently …ing\" calque; use a plain sentence (patterns B17)."),
    ("rhetorical_q", "W", True, re.compile(r"(آیا تا به حال|آماده‌اید\?|آماده‌اید؟|تصور کنید)"),
     "Rhetorical or throat-clearing question (patterns A6)."),
    ("pronoun_khod", "W", True, re.compile(r"\bشما می‌توانید .{0,40}خود "),
     "«شما … خود»; redundant pronoun (patterns B8)."),
    ("bare_cta", "W", False, re.compile(r"^(?:\s*)(شروع کنید|بیشتر بدانید|اکنون \S+ کنید)(?:\s*)$"),
     "Imperative CTA copied from an English button; check frames.md."),
    ("essay_opener", "E", True, re.compile(r"(در دنیای امروز|در عصر دیجیتال|در این (?:مقاله|متن|پست) به بررسی)"),
     "Clichéd essay-style opening; start with the claim (patterns A4)."),
    ("cliche_heading", "W", True, re.compile(r"^\s*(?:#+\s*)?(چرا باید \S+ را انتخاب کنید|مزایای استفاده از \S+)[؟?]?\s*$"),
     "Translated marketing/how-to heading; check frames.md (patterns A1)."),
    ("formal_future", "W", False, re.compile(r"\S+ خواهد (?:شد|کرد|گرفت|بود)"),
     "Formal future «خواهد …»; outside formal tone use the present (tones.md)."),
]

# fixed calques: (phrase, fix, severity)
CALQUES = [
    ("خوش برگشتید", "خوش آمدید / drop it", "E"),
    ("چیزی اشتباه پیش رفت", "مشکلی پیش آمد", "E"),
    ("ما اینجا هستیم تا کمک کنیم", "اگر مشکلی بود، به ما بگویید", "E"),
    ("موفقیت!", "انجام شد", "E"),
    ("چیزی برای نمایش وجود ندارد", "هنوز چیزی ثبت نشده", "E"),
    ("به جامعهٔ ما بپیوندید", "عضو … شوید", "E"),
    ("در پایان روز", "در نهایت / آخرش", "E"),
    ("قدرت‌گرفته از", "بر پایهٔ / با فناوری", "E"),
    ("سفر شما", "drop it; say it directly", "E"),
    ("تجربهٔ کاربری بی‌نظیر", "drop it", "E"),
    ("هرگونه سؤال", "سؤالی", "E"),
    ("به نظر می‌رسد که", "drop it", "E"),
    ("بدون هیچ‌گونه", "بدون", "E"),
    ("به سیستم وارد شوید", "وارد شوید", "E"),
    ("ما معتقدیم که", "drop it; state the claim", "E"),
    ("ما باور داریم که", "drop it; state the claim", "E"),
    # collocation calques
    ("معنی می‌دهد", "منطقی است / به کار می‌آید", "E"),
    ("معنا می‌دهد", "منطقی است / به کار می‌آید", "E"),
    ("تفاوت ایجاد کنید", "say the concrete result (make a difference)", "E"),
    ("زمانتان را ذخیره", "وقتتان کمتر هدر می‌رود (save time)", "E"),
    ("زمان شما را ذخیره", "وقتتان کمتر هدر می‌رود (save time)", "E"),
    ("به سطح بعدی", "say the concrete result (next level)", "E"),
    ("در قلب", "drop it if figurative (at the heart of)", "W"),
    ("ذهنی آسوده", "با خیال راحت", "E"),
    ("ذهن آسوده", "با خیال راحت", "E"),
    ("مطمئن شوید که", "حتماً … / دقت کنید که", "W"),
    ("هیجان‌زده‌ایم", "خوشحالیم / just give the news", "E"),
    ("یک کلیک و", "با یک کلیک … (one click and)", "E"),
    ("ما هستیم.", "به پشتیبانی بگویید (we're here)", "W"),
    ("راه‌حل‌های", "say exactly what it does (solutions)", "W"),
    ("قدرتمند", "say exactly what it does (powerful)", "W"),
    ("را تجربه کنید", "use a concrete verb (experience X)", "W"),
]

# document-level heuristics: they look at the whole text, not per line
EMOJI_BULLET = re.compile(r"^\s*[\U0001F300-\U0001FAFF☀-➿]\s*\S", re.MULTILINE)
BOLD_SPAN = re.compile(r"\*\*[^*\n]+\*\*")
CLICHE_CLOSING = re.compile(r"^\s*#*\s*(در پایان|جمع‌بندی)[:：]?\s*$", re.MULTILINE)
SENT_SPLIT = re.compile(r"[.!؟?]\s+")


def lint_document_level(text, fname="-"):
    """severity 'D': decorative tells that read as AI-generated at a glance."""
    hits = []
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return hits

    emoji_bullets = len(EMOJI_BULLET.findall(text))
    if emoji_bullets >= 3:
        hits.append(dict(file=fname, line=0, sev="D", rule="emoji_bullets", hook=True,
                         match=f"{emoji_bullets} lines with a leading emoji bullet",
                         msg="Decorative emoji before each bullet; Persian uses «-»/«•» or no marker (patterns A9)."))

    bold_spans = len(BOLD_SPAN.findall(text))
    if bold_spans >= 5 and len(lines) <= 40:
        hits.append(dict(file=fname, line=0, sev="D", rule="bold_overuse", hook=True,
                         match=f"{bold_spans} bolded spans",
                         msg="Too much bold; it pulls the reader off the sentence (patterns A9)."))

    closing = CLICHE_CLOSING.search(text)
    if closing and len(lines) <= 15:
        hits.append(dict(file=fname, line=0, sev="D", rule="cliche_closing", hook=True,
                         match=closing.group(0).strip(),
                         msg="Clichéd closing heading on a short text; probably unnecessary (patterns A9)."))

    # staccato: a paragraph of 3+ short sentences in a row (the user's main complaint)
    for ln, para in enumerate(text.split("\n\n")):
        if not re.search(PW, para) or SKIP_LINE.match(para):
            continue
        sents = [s for s in SENT_SPLIT.split(para.strip()) if re.search(PW, s)]
        run = 0
        for s in sents:
            words = len(re.findall(rf"{PW}+", s))
            run = run + 1 if 0 < words <= 7 else 0
            if run >= 3:
                hits.append(dict(file=fname, line=0, sev="D", rule="staccato", hook=True,
                                 match=para.strip()[:80] + "…",
                                 msg="Three short sentences in a row: clipped English rhythm. Stitch them together and explain (patterns B1)."))
                break
    return hits


SKIP_LINE = re.compile(r"^\s*(import |export |//|/\*|\*|<\?|#!)")
SKILL_ROOT = os.path.abspath(os.path.join(HERE, ".."))


def load_corpus():
    """Rows from references/terms.md and every file under references/terms/:
    | literal | write | source |. Rows whose fix says "correct, don't change"
    (or the older «درست است») are leave-alone notes and are skipped.
    The linter always reads every domain file, at no token cost, so a wrong
    domain guess while writing still gets caught here."""
    rows = []
    paths = [TERMS_CORE]
    if os.path.isdir(TERMS_DIR):
        paths += sorted(os.path.join(TERMS_DIR, fn) for fn in os.listdir(TERMS_DIR) if fn.endswith(".md"))
    for path in paths:
        try:
            lines = open(path, encoding="utf-8").read().splitlines()
        except Exception:
            continue
        for line in lines:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 3 or cells[2] not in SOURCES:
                continue
            if "correct, don't change" in cells[1] or "درست است" in cells[1]:
                continue
            for phrase in cells[0].split(" / "):
                phrase = re.sub(r"\s*\([^)]*\)", "", phrase)
                phrase = re.sub(r"(?:\s|^)(?:X|…)\.?(?=\s|$)", " ", phrase).strip(" .؟?")
                # single words (خوراک، اشاره، برچسب…) depend on meaning: too noisy for a linter
                if " " in norm(phrase):
                    rows.append(dict(phrase=phrase, equivalent=cells[1], source=SOURCES[cells[2]]))
    return rows


def norm(s):
    s = s.replace("‌", " ").replace("ي", "ی").replace("ك", "ک").replace("ٔ", "")
    return re.sub(r"\s+", " ", s)


def lint_text(text, corpus, fname="-", line_offset=0):
    hits = []
    for ln, line in enumerate(text.splitlines(), 1 + line_offset):
        if not re.search(PW, line) or SKIP_LINE.match(line):
            continue
        if "❌" in line:  # deliberate bad example
            continue
        for rid, sev, hook, rx, msg in MECH:
            for m in rx.finditer(line):
                hits.append(dict(file=fname, line=ln, sev=sev, rule=rid, hook=hook,
                                 match=m.group(0).strip(), msg=msg))
        nline = norm(line)
        for calque, fix, sev in CALQUES:
            if norm(calque) in nline:
                hits.append(dict(file=fname, line=ln, sev=sev, rule="calque", hook=True,
                                 match=calque, msg=f"Calque; write: {fix} (patterns C2/C4)."))
        for e in corpus:
            if norm(e["phrase"]) in nline:
                hits.append(dict(file=fname, line=ln, sev="W", rule="terms", hook=False,
                                 match=e["phrase"],
                                 msg=f"glossary ({e['source']}): → «{e['equivalent']}». If it means something else in this sentence, ignore it."))
    return hits


TONE_OFF = {
    "formal": {"semicolon", "formal_future"},
    "semi_formal": set(),
    "friendly": set(),
    "casual": set(),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-terms", action="store_true")
    ap.add_argument("--tone", choices=["formal", "semi_formal", "friendly", "casual"], default=None,
                    help="tone of the text; formal silences the «؛» and «خواهد» warnings")
    a = ap.parse_args()
    corpus = [] if a.no_terms else load_corpus()
    all_hits = []

    def run(text, name):
        return lint_text(text, corpus, name) + lint_document_level(text, name)

    for p in a.paths:
        if p != "-" and os.path.abspath(p).startswith(SKILL_ROOT):
            print(f"# {p}: inside the skill itself; its ❌ examples and calque tables are deliberately wrong. Skipped.", file=sys.stderr)
            continue
        if p == "-":
            all_hits += run(sys.stdin.read(), "-")
            continue
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fn in files:
                    if fn.endswith((".md", ".txt", ".tsx", ".jsx", ".ts", ".js", ".html", ".json", ".vue", ".php", ".po", ".yaml", ".yml")):
                        fp = os.path.join(root, fn)
                        try:
                            all_hits += run(open(fp, encoding="utf-8").read(), fp)
                        except UnicodeDecodeError:
                            pass
            continue
        all_hits += run(open(p, encoding="utf-8").read(), p)

    if a.tone:
        off = TONE_OFF[a.tone]
        all_hits = [h for h in all_hits if h["rule"] not in off]
    if a.json:
        print(json.dumps(all_hits, ensure_ascii=False, indent=1))
        return
    if not all_hits:
        print("hamghalam lint: nothing found.")
        return
    order = {"E": 0, "W": 1, "D": 2}
    all_hits.sort(key=lambda h: (order[h["sev"]], h["file"], h["line"]))
    label = {"E": "❌ almost always wrong", "W": "⚠️ check it", "D": "📄 document-level tell"}
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
    print(f"\n— {e} errors, {w} to check, {d} document-level. Nothing is auto-fixed.")


if __name__ == "__main__":
    main()
