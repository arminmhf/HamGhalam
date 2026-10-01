#!/usr/bin/env python3
"""
hamghalam lint — mechanical checks + translationese heuristics for Persian text.

Usage:
    python3 scripts/lint.py FILE [FILE ...]      # any text/tsx/jsx/html/md/json
    python3 scripts/lint.py -                    # read stdin
    python3 scripts/lint.py --json FILE          # machine-readable
    python3 scripts/lint.py --tone formal FILE   # tone-dependent rules adjust

Exit code is always 0; the report is for a human/model to judge, not a gate.
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
TERMS = os.path.join(HERE, "..", "references", "terms.md")

PERSIAN = "؀-ۿ‌"
PW = f"[{PERSIAN}]"
NB = f"(?<![{PERSIAN}])"   # not preceded by a Persian letter (word start)
NA = f"(?![{PERSIAN}])"    # not followed by a Persian letter (word end)
SENT = r"(?:^|[.!؟?»:]\s*|\n)"  # sentence start

# (id, severity, hook, regex, message)
MECH = [
    # ---- mechanical ----
    ("arabic_yeh_kaf", "E", True, re.compile(r"[يك]"),
     "حرف عربی «ي/ك»؛ «ی/ک» بنویس."),
    ("mi_space", "E", True, re.compile(rf"{NB}ن?می (?={PW})"),
     "«می» با فاصلهٔ کامل؛ نیم‌فاصله بگذار (می‌شود)."),
    ("mi_joined", "W", True, re.compile(rf"{NB}ن?می(?:شو|کن|تون|توان|ده|گیر|باش|رو|بین|خوا|یاب|رس|ساز|فرست)"),
     "«می» چسبیده (میشود)؛ نیم‌فاصله بگذار."),
    ("ha_space", "W", False, re.compile(rf"{PW}+ ها(?:ی|یی)?{NA}"),
     "جمع «ها» با فاصلهٔ کامل؛ احتمالاً نیم‌فاصله می‌خواهد (کتاب‌ها)."),
    ("latin_punct", "W", False, re.compile(rf"{PW}\s*[,;?]"),
     "نشانه‌گذاری انگلیسی بعد از واژهٔ فارسی؛ «،» «؛» «؟»."),
    ("straight_quotes", "W", False, re.compile(rf"(?<![=:(,\[{{])(?<![=:(,\[{{] )\"{PW}[^\"\n]{{1,80}}\""),
     "گیومهٔ انگلیسی دور متن فارسی؛ «…» بنویس."),
    ("latin_digits", "W", False, re.compile(rf"(?<![A-Za-z0-9_./:=\"'-])(?<![:=] )[0-9]+(?![A-Za-z0-9_./:-])(?=[^\n]*{PW})"),
     "عدد لاتین در متن فارسی؛ رقم فارسی بنویس (مگر کد/شناسه)."),
    ("slash_247", "E", True, re.compile(r"(?:۲۴|24)\s*/\s*(?:۷|7)"),
     "«۲۴/۷» کالک است؛ «شبانه‌روزی» بنویس."),

    # ---- sentence architecture ----
    ("tavassot", "E", True, re.compile(rf"{NB}توسط {PW}"),
     "مجهول با «توسط»؛ جمله را معلوم کن."),
    ("nominal", "W", True, re.compile(r"(اقدام به|انجام (?:دادن|شود|دهید)|مورد \S+ قرار|قابلیت \S+سازی|امکان‌پذیر می‌سازد)"),
     "اسم‌سازی؛ فعل ساده بنویس."),
    ("allows_you", "E", True, re.compile(r"(به شما (?:اجازه|امکان) می‌دهد|می‌تواند به شما کمک کند|کمک می‌کند تا)"),
     "کالک allows you to / helps you."),
    ("not_only", "E", True, re.compile(r"نه[ ‌]تنها .{2,60}بلکه"),
     "کالک not only … but also."),
    ("not_just", "E", True, re.compile(r"فقط یک [^.،؛\n]{1,40} نیست"),
     "کالک «It's not just X, it's Y»؛ مستقیم بگو چیست."),
    ("lets", "E", True, re.compile(rf"{NB}بیایید{NA}"),
     "«بیایید…» کالک Let's است."),
    ("cleft", "W", True, re.compile(r"این (?:شما|ما|او|آن‌ها|شمایید) (?:هستید|هستیم|است|هستند) که"),
     "جملهٔ برجسته‌ساز «این … است که» (It's you who …)؛ ساده بگو."),
    ("this_is_where", "E", True, re.compile(r"(?:اینجا|این‌جا)ست که"),
     "«اینجاست که … » کالک This is where … comes in."),
    ("this_means", "W", True, re.compile(rf"{SENT}این یعنی"),
     "شروع جمله با «این یعنی» (This means)؛ نتیجه را در خود جمله بگو."),
    ("indef_yek", "W", True, re.compile(rf"{NB}یک {PW}+(?: {PW}+)? (?:است|هستیم|هستید|هستند){NA}"),
     "«یک» نکرهٔ انگلیسی‌وار (a/an)؛ معمولاً «…ی است» طبیعی‌تر است (دستیار هوشمندی است)."),
    ("we_are_a", "W", True, re.compile(rf"{SENT}ما یک [^.\n]{{1,50}} هستیم"),
     "«ما یک … هستیم» (We are a …)؛ معرفی را با خود کار شروع کن."),
    ("with_using", "W", True, re.compile(rf"{SENT}با استفاده از"),
     "شروع جمله با «با استفاده از» (Using …)؛ معمولاً «با X» کافی است."),
    ("discourse_marker", "W", True, re.compile(rf"{SENT}(همچنین|علاوه بر این|به عبارت دیگر|در نتیجه|در واقع)،"),
     "قید ربطی انگلیسی‌وار در ابتدای جمله (Moreover/Additionally)؛ جمله را به قبلی بدوز یا قید را بردار."),
    ("intensifier", "W", False, re.compile(r"(واقعاً|به‌سادگی|به سادگی|به‌راحتی|به راحتی|به‌طور یکپارچه|به طور یکپارچه|به‌طور کامل|به طور کامل|به‌طور مؤثر|بی‌نظیر|در واقع)"),
     "قید تأکیدی ترجمه‌ای؛ احتمالاً حذف‌شدنی."),
    ("comma_before_va", "W", True, re.compile(r"[،,]\s*(?:و|یا)\s"),
     "ویرگول پیش از «و»/«یا»؛ در فهرست کالک Oxford comma است."),
    ("imperative_comma_reason", "W", False, re.compile(rf"{NB}(?:کنید|ببینید|بروید|بزنید|بگیرید|کن|ببین|برو|بزن)، \S+"),
     "دستور + توضیح با ویرگول؛ شاید نتیجه را مستقیم گفتن طبیعی‌تر باشد."),
    ("parenthetical_adverb", "W", True, re.compile(r"، (?:حتی|مثلاً|البته|گاهی|همیشه|هر روز|هر شب|نصف‌شب|نیمه‌شب|شب و روز|در صورت نیاز|به‌سرعت)[^،|«\n]{0,25}، "),
     "قید معترضه بین دو ویرگول؛ اول جمله یا کنار فعل بگذار."),
    ("you_just", "E", True, re.compile(r"(?:^|[.!؟?>]\s*|\sو\s)شما فقط \S+"),
     "ضربهٔ پایانی «شما فقط …» (You just …)."),
    ("punchline_only", "W", True, re.compile(r"(?:سهم|کار) شما فقط"),
     "ضربهٔ پایانی با واژه‌های دیگر؛ خودِ ترفند انگلیسی است، نه واژه‌اش."),
    ("tricolon", "W", True, re.compile(r"(?:می‌\S+|\S+د)، [^،.\n]{3,60}(?:می‌\S+|\S+د) و [^.\n]{3,80}(?:می‌\S+|\S+د)\."),
     "سه بند فعلی موازی بی‌فاعل؛ ریتم سه‌تایی تبلیغات انگلیسی."),
    ("semicolon", "W", False, re.compile(r"؛"),
     "«؛» در متن وب کم‌کاربرد است؛ اگر هر پاراگراف یکی دارد، ماشینی به نظر می‌رسد."),
    ("em_dash", "W", True, re.compile(r"—"),
     "خط تیرهٔ معترضه؛ با ویرگول یا «که» بگو."),
    ("colon_list", "W", True, re.compile(rf":\s*{PW}[^.\n]*،[^.\n]*(?:،| و ){PW}"),
     "دونقطه + فهرست؛ جملهٔ کامل بنویس."),
    ("dar_hal_hastid", "W", True, re.compile(r"در حال \S+ هستید"),
     "«در حال … هستید»؛ جملهٔ ساده بنویس."),
    ("rhetorical_q", "W", True, re.compile(r"(آیا تا به حال|آماده‌اید\?|آماده‌اید؟|تصور کنید)"),
     "سؤال بلاغی / مقدمه‌چینی."),
    ("pronoun_khod", "W", True, re.compile(r"\bشما می‌توانید .{0,40}خود "),
     "«شما … خود»؛ ضمیر اضافی."),
    ("bare_cta", "W", False, re.compile(r"^(?:\s*)(شروع کنید|بیشتر بدانید|اکنون \S+ کنید)(?:\s*)$"),
     "فراخوان امری کالک دکمهٔ انگلیسی."),
    ("essay_opener", "E", True, re.compile(r"(در دنیای امروز|در عصر دیجیتال|در این (?:مقاله|متن|پست) به بررسی)"),
     "افتتاحیهٔ مقاله‌ای کلیشه‌ای؛ مستقیم از ادعا شروع کن."),
    ("cliche_heading", "W", True, re.compile(r"^\s*(?:#+\s*)?(چرا باید \S+ را انتخاب کنید|مزایای استفاده از \S+)[؟?]?\s*$"),
     "تیتر ترجمه‌ای تبلیغاتی/آموزشی."),
    ("formal_future", "W", False, re.compile(r"\S+ خواهد (?:شد|کرد|گرفت|بود)"),
     "زمان آیندهٔ «خواهد …»؛ در لحن غیررسمی فعل حال بنویس."),
]

# fixed calques: (phrase, fix, severity)
CALQUES = [
    ("خوش برگشتید", "خوش آمدید / حذف", "E"),
    ("چیزی اشتباه پیش رفت", "مشکلی پیش آمد", "E"),
    ("ما اینجا هستیم تا کمک کنیم", "اگر مشکلی بود، به ما بگویید", "E"),
    ("موفقیت!", "انجام شد", "E"),
    ("چیزی برای نمایش وجود ندارد", "هنوز چیزی ثبت نشده", "E"),
    ("به جامعهٔ ما بپیوندید", "عضو … شوید", "E"),
    ("در پایان روز", "در نهایت / آخرش", "E"),
    ("قدرت‌گرفته از", "بر پایهٔ / با فناوری", "E"),
    ("سفر شما", "حذف؛ مستقیم بگو", "E"),
    ("تجربهٔ کاربری بی‌نظیر", "حذف", "E"),
    ("هرگونه سؤال", "سؤالی", "E"),
    ("به نظر می‌رسد که", "حذف", "E"),
    ("بدون هیچ‌گونه", "بدون", "E"),
    ("به سیستم وارد شوید", "وارد شوید", "E"),
    ("ما معتقدیم که", "حذف؛ مستقیم ادعا را بگو", "E"),
    ("ما باور داریم که", "حذف؛ مستقیم ادعا را بگو", "E"),
    # collocation calques
    ("معنی می‌دهد", "منطقی است / به کار می‌آید", "E"),
    ("معنا می‌دهد", "منطقی است / به کار می‌آید", "E"),
    ("تفاوت ایجاد کنید", "(کالک make a difference) نتیجهٔ مشخص را بگو", "E"),
    ("زمانتان را ذخیره", "(کالک save time) وقتتان کمتر هدر می‌رود", "E"),
    ("زمان شما را ذخیره", "(کالک save time) وقتتان کمتر هدر می‌رود", "E"),
    ("به سطح بعدی", "(کالک next level) نتیجهٔ مشخص را بگو", "E"),
    ("در قلب", "(کالک at the heart of) اگر معنای استعاری دارد، حذف کن", "W"),
    ("ذهنی آسوده", "با خیال راحت", "E"),
    ("ذهن آسوده", "با خیال راحت", "E"),
    ("مطمئن شوید که", "حتماً … / دقت کنید که", "W"),
    ("هیجان‌زده‌ایم", "خوشحالیم / مستقیم خبر را بده", "E"),
    ("یک کلیک و", "(کالک One click and) با یک کلیک …", "E"),
    ("ما هستیم.", "(کالک we're here) به پشتیبانی بگویید", "W"),
    ("راه‌حل‌های", "(کالک solutions) بگو دقیقاً چه کاری می‌کند", "W"),
    ("قدرتمند", "(کالک powerful) بگو دقیقاً چه کاری می‌کند", "W"),
    ("را تجربه کنید", "(کالک experience X) فعل مشخص بیاور", "W"),
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
                         match=f"{emoji_bullets} خط با ایموجی ابتدای بولت",
                         msg="ایموجی تزئینی قبل از بولت؛ فارسی با «-»/«•» یا بدون نشانه می‌نویسد."))

    bold_spans = len(BOLD_SPAN.findall(text))
    if bold_spans >= 5 and len(lines) <= 40:
        hits.append(dict(file=fname, line=0, sev="D", rule="bold_overuse", hook=True,
                         match=f"{bold_spans} عبارت بولدشده",
                         msg="بولدکردن بیش‌ازحد عبارات؛ خواننده را از خط جمله پرت می‌کند."))

    closing = CLICHE_CLOSING.search(text)
    if closing and len(lines) <= 15:
        hits.append(dict(file=fname, line=0, sev="D", rule="cliche_closing", hook=True,
                         match=closing.group(0).strip(),
                         msg="جمع‌بندی کلیشه‌ای در متن کوتاه؛ احتمالاً لازم نیست."))

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
                                 msg="سه جملهٔ کوتاه پشت هم؛ ریتم بریدهٔ انگلیسی. جمله‌ها را به هم بدوز و توضیح بده."))
                break
    return hits


SKIP_LINE = re.compile(r"^\s*(import |export |//|/\*|\*|<\?|#!)")
SKILL_ROOT = os.path.abspath(os.path.join(HERE, ".."))


def load_corpus():
    """Rows of references/terms.md: | literal | write | source |.
    Rows whose fix says «درست است» are "leave alone" notes and are skipped."""
    rows = []
    try:
        lines = open(TERMS, encoding="utf-8").read().splitlines()
    except Exception:
        return rows
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[2] not in ("🔵", "🟢", "✍️") or "درست است" in cells[1]:
            continue
        for phrase in cells[0].split(" / "):
            phrase = re.sub(r"\s*\([^)]*\)", "", phrase)
            phrase = re.sub(r"(?:\s|^)(?:X|…)\.?(?=\s|$)", " ", phrase).strip(" .؟?")
            # single words are meaning-dependent: too noisy for a linter
            if " " in norm(phrase):
                rows.append(dict(phrase=phrase, equivalent=cells[1],
                                 source={"🔵": "ویراستاری", "🟢": "جامعه", "✍️": "کپی‌رایتر"}[cells[2]]))
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
                                 match=calque, msg=f"کالک؛ بنویس: {fix}."))
        for e in corpus:
            if norm(e["phrase"]) in nline:
                hits.append(dict(file=fname, line=ln, sev="W", rule="terms", hook=False,
                                 match=e["phrase"],
                                 msg=f"terms.md ({e['source']}): → «{e['equivalent']}». اگر در این جمله معنای دیگری دارد، رد کن."))
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
                    help="لحن متن؛ با formal هشدار «؛» و «خواهد» خاموش می‌شود")
    a = ap.parse_args()
    corpus = [] if a.no_terms else load_corpus()
    all_hits = []

    def run(text, name):
        return lint_text(text, corpus, name) + lint_document_level(text, name)

    for p in a.paths:
        if p != "-" and os.path.abspath(p).startswith(SKILL_ROOT):
            print(f"# {p}: داخل خود اسکیل است؛ مثال‌های ❌ و جدول‌های کالک عمداً ایراد دارند. رد شد.", file=sys.stderr)
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
        print("hamghalam lint: چیزی پیدا نشد.")
        return
    order = {"E": 0, "W": 1, "D": 2}
    all_hits.sort(key=lambda h: (order[h["sev"]], h["file"], h["line"]))
    label = {"E": "❌ تقریباً همیشه ایراد", "W": "⚠️ بررسی کن", "D": "📄 نشانهٔ ساختاری سند"}
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
    print(f"\n— {e} ایراد، {w} مورد بررسی، {d} نشانهٔ ساختاری سند. هیچ‌کدام خودکار اصلاح نمی‌شود.")


if __name__ == "__main__":
    main()
