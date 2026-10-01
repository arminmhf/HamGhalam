#!/usr/bin/env python3
"""
hamghalam lint — mechanical checks + glossary matching for Persian text.

Usage:
    python3 scripts/lint.py FILE [FILE ...]      # any text/tsx/jsx/html/md/json
    python3 scripts/lint.py -                    # read stdin
    python3 scripts/lint.py --json FILE          # machine-readable

Exit code is always 0; the report is for a human/model to judge, not a gate.
Checks are heuristics. Every hit needs eyes; nothing here is auto-fixable.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TERMS = os.path.join(HERE, "..", "references", "terms.md")

PERSIAN = "\u0600-\u06FF\u200c"
PW = f"[{PERSIAN}]"

# ---- mechanical rules -------------------------------------------------------
# (id, severity, regex, message)   severity: E = almost always wrong, W = check
MECH = [
    ("arabic_yeh_kaf", "E", re.compile(r"[\u064a\u0643]"),
     "حرف عربی «ي/ك»؛ «ی/ک» بنویس."),
    ("mi_space", "E", re.compile(rf"(?<![{PERSIAN}])ن?می (?={PW})"),
     "«می» با فاصلهٔ کامل؛ نیم‌فاصله بگذار (می‌شود)."),
    ("mi_joined", "W", re.compile(rf"(?<![{PERSIAN}])ن?می(?:شو|کن|تون|توان|ده|گیر|باش|رو|بین|خوا|یاب|رس|ساز|فرست)"),
     "«می» چسبیده (میشود)؛ نیم‌فاصله بگذار."),
    ("ha_space", "W", re.compile(rf"{PW}+ ها(?:ی|یی)?(?![{PERSIAN}])"),
     "جمع «ها» با فاصلهٔ کامل؛ احتمالاً نیم‌فاصله می‌خواهد (کتاب‌ها)."),
    ("latin_punct", "W", re.compile(rf"{PW}\s*[,;?]"),
     "نشانه‌گذاری انگلیسی بعد از واژهٔ فارسی؛ «،» «؛» «؟»."),
    ("straight_quotes", "W", re.compile(rf"(?<![=:(,\[{{])(?<![=:(,\[{{] )\"{PW}[^\"\n]{{1,80}}\""),
     "گیومهٔ انگلیسی دور متن فارسی؛ «…» بنویس."),
    ("latin_digits", "W", re.compile(rf"(?<![A-Za-z0-9_./:=\"'-])(?<![:=] )[0-9]+(?![A-Za-z0-9_./:-])(?=[^\n]*{PW})"),
     "عدد لاتین در متن فارسی؛ رقم فارسی بنویس (مگر کد/شناسه)."),
    ("tavassot", "E", re.compile(rf"\bتوسط {PW}"),
     "مجهول با «توسط»؛ جمله را معلوم کن (الگوی ۴)."),
    ("nominal", "W", re.compile(r"(اقدام به|انجام (?:دادن|شود|دهید)|مورد \S+ قرار|قابلیت \S+سازی|امکان‌پذیر می‌سازد)"),
     "اسم‌سازی؛ فعل ساده بنویس (الگوی ۵)."),
    ("allows_you", "E", re.compile(r"(به شما (?:اجازه|امکان) می‌دهد|می‌تواند به شما کمک کند|کمک می‌کند تا)"),
     "کالک allows you to / helps you (الگوی ۶)."),
    ("not_only", "E", re.compile(r"نه[ \u200c]تنها .{2,60}بلکه"),
     "کالک not only … but also (الگوی ۸)."),
    ("intensifier", "W", re.compile(r"(واقعاً|به‌سادگی|به سادگی|به‌راحتی|به راحتی|به‌طور یکپارچه|به طور یکپارچه|به‌طور کامل|به طور کامل|به‌طور مؤثر|بی‌نظیر|در واقع)"),
     "قید تأکیدی ترجمه‌ای؛ احتمالاً حذف‌شدنی (الگوی ۹)."),
    ("comma_before_va", "E", re.compile(r"[،,]\s*(?:و|یا)\s"),
     "ویرگول پیش از «و»/«یا»؛ کالک Oxford comma. ویرگول را بردار یا جمله را با نقطه ببند (قاعدهٔ ۷)."),
    ("imperative_comma_reason", "W", re.compile(r"(?:کنید|ببینید|بروید|بزنید|بگیرید|کن|ببین|برو|بزن)، \S+"),
     "دستور + توضیح با ویرگول؛ احتمالاً نتیجه را مستقیم بگو (الگوی ۱۶) یا نقطه بگذار (الگوی ۱۷)."),
    ("parenthetical_adverb", "W", re.compile(r"، (?:حتی|مثلاً|البته|گاهی|همیشه|هر روز|هر شب|نصف‌شب|شب و روز|در صورت نیاز|به‌سرعت)[^،|«\n]{0,25}، "),
     "قید معترضه بین دو ویرگول؛ اول جمله یا کنار فعل بگذار (الگوی ۱۸)."),
    ("you_just", "E", re.compile(r"(?:^|[.!؟?>]\s*)شما فقط \S+"),
     "ضربهٔ پایانی «شما فقط …»؛ کالک You just (الگوی ۲۰)."),
    ("tricolon", "W", re.compile(r"(?:می‌\S+|\S+د)، [^،.\n]{3,60}(?:می‌\S+|\S+د) و [^.\n]{3,80}(?:می‌\S+|\S+د)\."),
     "سه بند فعلی موازی؛ اگر فاعل ندارد، سه‌گانهٔ انگلیسی است (الگوی ۱۹)."),
    ("semicolon", "W", re.compile(r"؛"),
     "نقطه‌ویرگول «؛» فقط در لحن رسمی؛ در بقیه نقطه یا «و» (قاعدهٔ ۶)."),
    ("em_dash", "W", re.compile(r"—"),
     "خط تیرهٔ معترضه؛ با ویرگول یا «که» بگو (الگوی ۱۱)."),
    ("colon_list", "W", re.compile(rf":\s*{PW}[^.\n]*،[^.\n]*(?:،| و ){PW}"),
     "دونقطه + فهرست؛ جملهٔ کامل بنویس (الگوی ۱)."),
    ("dar_hal_hastid", "W", re.compile(r"در حال \S+ هستید"),
     "«در حال … هستید»؛ جملهٔ ساده (الگوی ۱۴)."),
    ("rhetorical_q", "W", re.compile(r"(آیا تا به حال|آماده‌اید\?|آماده‌اید؟|تصور کنید)"),
     "سؤال بلاغی / مقدمه‌چینی (الگوی ۱۳)."),
    ("pronoun_khod", "W", re.compile(r"\bشما می‌توانید .{0,40}خود "),
     "«شما … خود»؛ ضمیر اضافی (الگوی ۷)."),
    ("bare_cta", "W", re.compile(r"^(?:\s*)(شروع کنید|بیشتر بدانید|اکنون \S+ کنید)(?:\s*)$"),
     "فراخوان امری برهنه؛ دکمهٔ فارسی مصدر/اسم است (الگوی ۱۲)."),
]

# pattern 15 calques
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
}

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
        if len(cells) != 3 or cells[2] not in ("🔵", "🟢") or "درست است" in cells[1]:
            continue
        for phrase in cells[0].split(" / "):
            phrase = re.sub(r"\s*\([^)]*\)", "", phrase)
            phrase = re.sub(r"(?:\s|^)(?:X|…)\.?(?=\s|$)", " ", phrase).strip(" .؟?")
            # single words (خوراک، اشاره، برچسب، جامعه…) are meaning-dependent: too noisy for a linter
            if " " in norm(phrase):
                rows.append(dict(phrase=phrase, equivalent=cells[1],
                                 source="ویراستاری" if cells[2] == "🔵" else "جامعه"))
    return rows


def norm(s):
    s = s.replace("\u200c", " ").replace("ي", "ی").replace("ك", "ک").replace("ٔ", "")
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
                                 match=calque, msg=f"کالک؛ بنویس: {fix} (الگوی ۱۵)."))
        for e in corpus:
            if norm(e["phrase"]) in nline:
                hits.append(dict(file=fname, line=ln, sev="W", rule="terms",
                                 match=e["phrase"],
                                 msg=f"terms.md ({e['source']}): → «{e['equivalent']}». اگر در این جمله معنای دیگری دارد، رد کن."))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-terms", action="store_true")
    ap.add_argument("--tone", choices=["formal", "semi_formal", "friendly", "casual"], default=None,
                    help="لحن متن؛ با formal هشدار «؛» خاموش می‌شود")
    a = ap.parse_args()
    corpus = [] if a.no_terms else load_corpus()
    all_hits = []
    for p in a.paths:
        if p != "-" and os.path.abspath(p).startswith(SKILL_ROOT):
            print(f"# {p}: داخل خود اسکیل است؛ مثال‌های ❌ و جدول‌های کالک عمداً ایراد دارند. رد شد.", file=sys.stderr)
            continue
        if p == "-":
            all_hits += lint_text(sys.stdin.read(), corpus, "-")
            continue
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fn in files:
                    if fn.endswith((".md", ".txt", ".tsx", ".jsx", ".ts", ".js", ".html", ".json", ".vue", ".php", ".po", ".yaml", ".yml")):
                        fp = os.path.join(root, fn)
                        try:
                            all_hits += lint_text(open(fp, encoding="utf-8").read(), corpus, fp)
                        except UnicodeDecodeError:
                            pass
            continue
        all_hits += lint_text(open(p, encoding="utf-8").read(), corpus, p)

    if a.tone == "formal":
        all_hits = [h for h in all_hits if h["rule"] != "semicolon"]
    if a.json:
        print(json.dumps(all_hits, ensure_ascii=False, indent=1))
        return
    if not all_hits:
        print("hamghalam lint: چیزی پیدا نشد.")
        return
    order = {"E": 0, "W": 1}
    all_hits.sort(key=lambda h: (order[h["sev"]], h["file"], h["line"]))
    label = {"E": "❌ تقریباً همیشه ایراد", "W": "⚠️ بررسی کن"}
    cur = None
    for h in all_hits:
        if h["sev"] != cur:
            cur = h["sev"]
            print(f"\n## {label[cur]}\n")
        print(f"{h['file']}:{h['line']}  [{h['rule']}]  «{h['match']}»\n    {h['msg']}")
    e = sum(1 for h in all_hits if h["sev"] == "E")
    w = sum(1 for h in all_hits if h["sev"] == "W")
    print(f"\n— {e} ایراد، {w} مورد بررسی. هیچ‌کدام خودکار اصلاح نمی‌شود.")


if __name__ == "__main__":
    main()
