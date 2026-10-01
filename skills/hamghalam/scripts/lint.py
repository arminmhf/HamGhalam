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
# Every rule here was checked against a Persian copywriter's review (2026-10-01).
# Rules the copywriter rejected (توسط، نه تنها … بلکه، rhetorical questions, colon lists,
# «در حال … هستید»، essay openers, discourse markers, verbless fragments) were removed:
# flagging normal Persian pushes the model into over-correcting.
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
     "«۲۴/۷» is a calque of 24/7; write «۲۴ ساعته» or «شبانه‌روزی» (patterns C2)."),
    ("comma_before_va", "E", True, re.compile(r"[،,]\s*(?:و|که)\s"),
     "Comma before «و» or «که»; never in Persian (mechanics 6)."),
    ("comma_before_ya", "W", False, re.compile(r"[،,]\s*یا\s"),
     "Comma before «یا»; in a list it's the Oxford comma calque."),
    ("semicolon", "W", False, re.compile(r"؛"),
     "«؛» only sparingly, and not in friendly or casual tone (mechanics 8)."),
    ("em_dash", "W", True, re.compile(r"—"),
     "Em dash as a parenthetical; use commas (an appositive) or «که» (patterns B9)."),

    # ---- register ----
    ("spoken_register", "W", True, re.compile(r"(خبرتان می‌کنیم|خبرت می‌کنیم|جلویتان می‌گذار|حواسش به|حواسمان به|درست‌وحسابی|درست و حسابی|گیر کردید|گیر کرد)"),
     "Spoken idiom; fine in friendly/casual, but semi-formal and formal copy use written verbs (اطلاع می‌دهیم، مراقب … است) (patterns A1)."),
    ("formal_future", "W", False, re.compile(r"\S+ خواهد (?:شد|کرد|گرفت|بود)"),
     "Formal future «خواهد …»; heavy outside formal tone, use the present (tones.md)."),

    # ---- frames and closing ----
    ("bad_frame", "W", True, re.compile(r"(چه کار(?:ی|هایی) برایتان انجام می‌دهد|چه باری از دوشتان|آماده‌اید شروع کنید|با \S+ چه کارهایی می‌توانید بکنید)"),
     "Translated section frame; use frames.md (patterns A2)."),
    ("bad_frame_heading", "W", True, re.compile(r"^\s*(?:#+\s*)?(مأموریت ما|با ما در تماس باشید|در خبرنامهٔ ما مشترک شوید|روش کار|ویژگی‌ها|قابلیت‌ها)\s*[؟?]?\s*$"),
     "Heading the copywriter didn't pick; see frames.md (patterns A2)."),
    ("bare_cta", "W", True, re.compile(r"(?:^\s*|[\"'>]\s*)(شروع کنید|همین حالا شروع کنید|بیشتر بدانید|رایگان امتحان کنید|امتحان رایگان)(?:\s*$|\s*[\"'<])"),
     "Button text the copywriter rejected; use «شروع»، «ثبت‌نام رایگان»، «اطلاعات بیشتر» (frames.md)."),
    ("you_just", "E", True, re.compile(r"(?:^|[.!؟?>]\s*|\sو\s)شما فقط \S+"),
     "Terse closing line with the reader as subject («شما فقط … می‌بینید»); end with a full sentence (patterns A3)."),

    # ---- sentence ----
    ("allows_you", "E", True, re.compile(r"(به شما (?:اجازه|امکان) می‌دهد تا|می‌تواند به شما کمک کند تا|کمک می‌کند تا)"),
     "Calque of \"allows you to\" / \"helps you\" (patterns B4)."),
    ("pronoun_khod", "W", True, re.compile(r"\bشما می‌توانید .{0,40}خود "),
     "«شما … خود»; pronoun spraying (patterns B5)."),
    ("nominal", "W", True, re.compile(r"(اقدام به|انجام (?:دادن|شود|دهید))"),
     "«اقدام به» / «انجام …» nominalization; use the plain verb (patterns B6)."),
    ("cleft", "E", True, re.compile(r"این (?:شما|ما|او|آن‌ها|شمایید) (?:هستید|هستیم|است|هستند) که"),
     "Cleft «این … است که» (\"It's you who …\"); say it plainly (patterns B7)."),
    ("parenthetical_adverb", "W", True, re.compile(r"، (?:حتی|مثلاً|البته|گاهی|همیشه|هر روز|هر شب|نصف‌شب|نیمه‌شب|شب و روز|در صورت نیاز|به‌سرعت)[^،|«\n]{0,25}، "),
     "Adverb wedged between two commas; rare in Persian, put it at the start or next to the verb (patterns B10)."),
    ("intensifier", "W", False, re.compile(r"(واقعاً|به‌سادگی|به سادگی|به‌راحتی|به راحتی|به‌طور یکپارچه|به طور یکپارچه|به‌طور کامل|به طور کامل|به‌طور مؤثر|بی‌نظیر)"),
     "Translated intensifier; probably droppable (patterns C1)."),
    ("imperative_comma_reason", "W", False, re.compile(rf"{NB}(?:ببینید|بروید|بزنید|کن|ببین|برو|بزن)، \S+"),
     "Imperative + comma-attached reason; stating the result may read better («لینک تأیید ایمیل شد.»)."),

    # ---- fine once, a tell when repeated (reported only at 2+ per text; patterns A7) ----
    ("indef_yek", "W", True, re.compile(rf"{NB}یک {PW}+(?: {PW}+)? (?:است|هستیم|هستید|هستند){NA}"),
     "«یک» as an indefinite article, more than once; «…ی است» is often more natural (patterns A7)."),
    ("we_are_a", "W", True, re.compile(rf"{SENT}ما یک [^.\n]{{1,50}} هستیم"),
     "«ما یک … هستیم», more than once (patterns A7)."),
    ("lets", "W", True, re.compile(rf"{NB}بیایید{NA}"),
     "«بیایید…», more than once (patterns A7)."),
    ("not_just", "W", True, re.compile(r"فقط یک [^.،؛\n]{1,40} نیست"),
     "«این فقط X نیست، Y است», more than once (patterns A7)."),
]
REPEAT_ONLY = {"indef_yek", "we_are_a", "lets", "not_just"}

# fixed calques: (phrase, fix, severity). The fixes are the copywriter's (patterns C2, C4).
CALQUES = [
    ("خوش برگشتید", "خوش آمدید", "E"),
    ("چیزی اشتباه پیش رفت", "مشکلی پیش آمد", "E"),
    ("ما اینجا هستیم تا کمک کنیم", "اگر مشکلی بود، به ما بگویید", "E"),
    ("موفقیت!", "انجام شد / ذخیره شد", "E"),
    ("چیزی برای نمایش وجود ندارد", "هنوز چیزی ثبت نشده / لیست … خالی است", "E"),
    ("به جامعهٔ ما بپیوندید", "عضو … شوید", "E"),
    ("در پایان روز", "در نهایت", "E"),
    ("قدرت‌گرفته از", "بر پایهٔ / با فناوری", "E"),
    ("هرگونه سؤال", "سؤالی", "E"),
    ("بدون هیچ‌گونه", "بدون", "E"),
    ("به سیستم وارد شوید", "وارد شوید", "E"),
    ("سفر شما", "usually drop it", "W"),
    ("تجربهٔ کاربری بی‌نظیر", "usually drop it", "W"),
    ("به نظر می‌رسد که", "usually drop it", "W"),
    ("ما معتقدیم که", "usually drop it", "W"),
    ("ما باور داریم که", "usually drop it", "W"),
    # collocation calques
    ("تفاوت ایجاد کنید", "«… را متفاوت کنید»", "E"),
    ("زمانتان را ذخیره", "«در زمان صرفه‌جویی کنید»", "E"),
    ("زمان شما را ذخیره", "«در زمان صرفه‌جویی کنید»", "E"),
    ("به سطح بعدی", "«ارتقا دهید»", "E"),
    ("ذهنی آسوده", "«با خیال راحت»", "E"),
    ("ذهن آسوده", "«با خیال راحت»", "E"),
    ("مطمئن شوید که", "«از صحت … مطمئن شوید» or state the problem («آدرس واردشده صحیح نیست»)", "E"),
    ("هیجان‌زده‌ایم", "«مفتخریم که …»", "E"),
    ("یک کلیک و", "«… بلافاصله فعال می‌شود»", "E"),
    ("کرمای طلایی", "translated product imagery; say what it does (patterns C3)", "E"),
    ("تا با هم انتخاب کنیم", "«تا کمکتان کنیم»", "E"),
]
# «ما هستیم» is fine in friendly/casual only; checked separately so --tone can silence it
WE_ARE_HERE = re.compile(r"(?:،|\s)ما هستیم[.!]")

# document-level heuristics: they look at the whole text, not per line
EMOJI_BULLET = re.compile(r"^\s*[\U0001F300-\U0001FAFF☀-➿]\s*\S", re.MULTILINE)
BOLD_SPAN = re.compile(r"\*\*[^*\n]+\*\*")
CLICHE_CLOSING = re.compile(r"^\s*#*\s*(در پایان|جمع‌بندی)[:：]?\s*$", re.MULTILINE)
SENT_SPLIT = re.compile(r"[.!؟?]\s+")
VERB_END = re.compile(r"(?:است|اند|ایم|اید|ند|یم|ید|د|شد)$")
CONNECTORS = {"برای همین": "برای همین", "به همین دلیل": "به همین دلیل", "بنابراین": "بنابراین", "در نتیجه": "در نتیجه", "پس": "پس(?! از)"}


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

    closings = len(re.findall(rf"{NB}در نهایت،?", text))
    if closings >= 2:
        hits.append(dict(file=fname, line=0, sev="D", rule="closing_formula", hook=True,
                         match=f"«در نهایت» ×{closings}",
                         msg="«در نهایت …» used as a closing more than once; it's one way to end, not a template (patterns A3)."))

    # staccato: a paragraph of 3+ short sentences in a row (the user's main complaint)
    for ln, para in enumerate(text.split("\n\n")):
        if not re.search(PW, para) or SKIP_LINE.match(para):
            continue
        sents = [s for s in SENT_SPLIT.split(para.strip()) if re.search(PW, s)]
        run = 0
        for s in sents:
            words = re.findall(rf"{PW}+", s)
            # only short sentences that end in a verb count; verbless phrases
            # («نصب سریع، حجم کم») are a normal Persian short form
            verb_end = bool(words) and VERB_END.search(words[-1])
            run = run + 1 if 0 < len(words) <= 7 and verb_end else 0
            if run >= 3:
                hits.append(dict(file=fname, line=0, sev="D", rule="staccato", hook=True,
                                 match=para.strip()[:80] + "…",
                                 msg="Three short sentences in a row: clipped English rhythm. Stitch them together and explain (patterns B1)."))
                break
        # the same connector stitched onto sentence after sentence is its own monotone rhythm
        counts = {c: len(re.findall(rf"{NB}{rx}{NA}", para)) for c, rx in CONNECTORS.items()}
        top = max(counts, key=counts.get)
        if counts[top] >= 3 or sum(counts.values()) >= max(3, len(sents) // 2):
            hits.append(dict(file=fname, line=0, sev="D", rule="connector_repeat", hook=True,
                             match=f"«{top}» ×{counts[top]}",
                             msg="The same connector on sentence after sentence (برای همین… پس… برای همین…) is a formula too. Vary how clauses join, and not every feature needs a benefit clause (patterns A8)."))
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
        for m in WE_ARE_HERE.finditer(line):
            hits.append(dict(file=fname, line=ln, sev="W", rule="we_are_here", hook=True,
                             match=m.group(0).strip(" ،"),
                             msg="«ما هستیم» is fine in friendly/casual tone only; in semi-formal write «می‌توانید با ما در ارتباط باشید» (patterns C2)."))
        for e in corpus:
            if norm(e["phrase"]) in nline:
                hits.append(dict(file=fname, line=ln, sev="W", rule="terms", hook=False,
                                 match=e["phrase"],
                                 msg=f"glossary ({e['source']}): → «{e['equivalent']}». If it means something else in this sentence, ignore it."))
    # fine once, a tell when repeated: drop these unless they occur at least twice in this text
    counts = {}
    for h in hits:
        if h["rule"] in REPEAT_ONLY:
            counts[h["rule"]] = counts.get(h["rule"], 0) + 1
    return [h for h in hits if h["rule"] not in REPEAT_ONLY or counts[h["rule"]] >= 2]


TONE_OFF = {
    "formal": {"semicolon", "formal_future"},
    "semi_formal": {"semicolon"},
    "friendly": {"spoken_register", "we_are_here"},
    "casual": {"spoken_register", "we_are_here"},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-terms", action="store_true")
    ap.add_argument("--tone", choices=["formal", "semi_formal", "friendly", "casual"], default=None,
                    help="tone of the text: formal/semi_formal silence the «؛» warning; friendly/casual allow spoken idioms and «ما هستیم»")
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
