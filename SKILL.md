---
name: hamghalam
description: نوشتن و ویرایش فارسی بومی (نه ترجمه‌ای) برای متن سایت، محصول، پیام خطا، ایمیل و تبلیغ، با لحن انتخابی؛ حتی وقتی این متن فقط یک رشتهٔ کوچک داخل کدی است که برای یک تسک دیگر می‌نویسی (لیبل دکمه، placeholder، پیام خطا در یک کامپوننت). Use whenever writing, rewriting or reviewing Persian (Farsi) copy of any kind — UI strings, landing pages, product descriptions, error messages, emails, marketing, docs — or whenever the user complains that Persian output sounds translated, machine-like, or "English in Persian words". Also applies to incidental Persian strings written inside otherwise non-Persian coding tasks (a button label, a form placeholder, a toast message in a component you're building).
---

# Hamghalam: Persian people actually write

The problem with the Persian LLMs write usually isn't vocabulary; it's **sentence architecture**. The words are Persian but the sentence is still thinking in English. This skill gives you three things: a list of translation-tell patterns to recognize, a process for writing and editing, and a small term glossary (`references/terms.md` plus domain files under `references/terms/`).

**The core test, everywhere:** if you can guess the English sentence behind a Persian sentence, it's translated.

## Step zero: tone and mode

- **Mode:** writing (new text) or editing (existing text). Each has its own process below.
- **Tone:** formal | semi-formal | friendly | casual. If it's not clear from the user's request or the project's existing copy, ask. If you get no answer, default to semi-formal and say in your output that you assumed it. Tone guide in `references/tones.md`.
- **Domain** matters only for picking terms. Figure it out from the user's request or the project's existing content, then read the matching file(s) under `references/terms/` (`tech.md`, `finance.md`, `retail.md`, …) — if you're unsure which domain fits, or the text spans more than one, read all plausible candidates; each file is small. Always read the core `references/terms.md` regardless. See "Domain-specific lists" in that file for why this is lazy and why it's safe to guess wrong.

## Translation-tell patterns

Each pattern has a pair of examples. Recognize ❌; model ✅. The ❌ example is a "sample of the mistake," not text to imitate.

**1. Colon + list of noun phrases.** English writes "X: a, b, and c." Persian says the same thing as a full sentence.
❌ سه مزیت دارد: سرعت بالا، نصب آسان و پشتیبانی ۲۴ ساعته.
✅ سریع است، راحت نصب می‌شود و پشتیبانی‌اش هم شبانه‌روزی است.

**2. Verbless sentence fragments.** A noun phrase punctuated like a sentence. Give it a verb.
❌ سریع. امن. بدون دردسر.
✅ هم سریع است، هم امن، دردسر هم ندارد.
This pattern is for **body copy**. Headlines, taglines, image captions, table labels and feature-card titles are verbless in Persian too and shouldn't get a verb forced in: «همیشه رقابتی، هرگز زیر کف»، «سئو، بدون کارشناس سئو»، «هر پاسخ حدود ۸۵۰ توکن، در چند ثانیه» are all fine as is. Test: would a Persian newspaper ad headline be written this way? If yes, leave it. What's still wrong even in a headline: a string of single-word fragments punctuated like sentences («سریع. امن. ساده.») and the "X, reimagined" slogan calque.

**3. Choppy consecutive sentences and tricolon rhythm.** Three five-word sentences in a row is English web rhythm. Persian stretches the sentence and stitches pieces together with «و», «که» and commas.
❌ سریع نصب می‌شود. حجمش کم است. آپدیت خودکار دارد.
✅ سریع نصب می‌شود و حجمش هم کم است، آپدیت را هم خودش می‌گیرد.

**4. Passive with «توسط».** The subject is known, so make the sentence active. The subjectless passive («لینک ارسال شد») is natural and fine in formal and semi-formal tone.
❌ این گزارش توسط تیم پشتیبانی بررسی می‌شود.
✅ تیم پشتیبانی این گزارش را بررسی می‌کند.

**5. Nominalization.** «انجام X», «اقدام به X», «مورد X قرار گرفتن», «قابلیت X‌سازی» instead of a plain verb.
❌ برای انجام ثبت‌نام، اقدام به وارد کردن شماره تلفن کنید.
✅ برای ثبت‌نام، شماره تلفنتان را وارد کنید.

**6. "Allows you to" / "can help you."** Calque of allows you to / can help you. Make the user the subject, or bring the tool in with «با».
❌ این ابزار به شما اجازه می‌دهد تا گزارش‌ها را دانلود کنید.
✅ گزارش‌ها را از همین‌جا دانلود کنید. / با این ابزار گزارش‌ها را دانلود می‌کنید.

**7. Redundant pronoun.** «شما», «ما», «خود», «آن» where Persian drops the pronoun.
❌ شما می‌توانید تنظیمات خود را در پنل کاربری خود تغییر دهید.
✅ تنظیمات را از پنل کاربری تغییر دهید.

**8. "Not only … but also."** Calque of not only … but also. Persian says «هم … هم» or doesn't say it at all.
❌ نه تنها سریع است، بلکه امن نیز هست.
✅ هم سریع است، هم امن.

**9. Translated intensifier adverbs.** واقعاً, به‌سادگی, به‌راحتی, به‌طور یکپارچه, به‌طور کامل, کاملاً, در واقع, به‌طور مؤثر, بی‌نظیر. Drop most of them; the sentence is stronger without them.
❌ به‌سادگی می‌توانید به‌طور یکپارچه با ابزارهای خود ادغام شوید.
✅ به ابزارهایی که دارید وصل می‌شود.

**10. Ezafe chain (stacked genitives).** Three ezafes in a row instead of a predicate or preposition.
❌ عبارت‌های ترجمه‌ای متن‌های هوش مصنوعی را جمع می‌کند.
✅ عبارت‌های ترجمه‌ای را از متن‌های هوش مصنوعی جمع می‌کند.

**11. Parenthetical em dash.** «—» is English. Use a comma, «که», or a separate sentence instead.
❌ رصدبان — ابزار پایش قیمت رقبا — رایگان شد.
✅ رصدبان که قیمت رقبا را پایش می‌کند، رایگان شد.

**12. Bare imperative CTA.** «شروع کنید.» «بیشتر بدانید.» «اکنون ثبت‌نام کنید.» This is a calque of English button copy. A Persian button uses an infinitive or a noun.
❌ شروع کنید | بیشتر بدانید | اکنون ثبت‌نام کنید
✅ شروع | اطلاعات بیشتر | ثبت‌نام / همین حالا ثبت‌نام کنید

**13. Rhetorical question / throat-clearing.** «آیا تا به حال…؟», «آماده‌اید؟», «تصور کنید…». Drop it and start with the actual point.
❌ آیا تا به حال به این فکر کرده‌اید که چطور می‌توانید قیمت رقبا را رصد کنید؟
✅ قیمت رقبا را چطور رصد می‌کنید؟

**14. "You are currently …ing" and translated status phrasing.** «شما در حال مشاهدهٔ X هستید» instead of a plain sentence.
❌ شما در حال مشاهدهٔ نسخهٔ آزمایشی هستید.
✅ این نسخهٔ آزمایشی است.

**15. Calqued boilerplate phrases.** Change these unconditionally:

| Calque | Write instead |
|---|---|
| خوش برگشتید! | خوش آمدید / (drop it) |
| چیزی اشتباه پیش رفت | مشکلی پیش آمد |
| ما اینجا هستیم تا کمک کنیم | اگر مشکلی بود، به ما بگویید / پشتیبانی پاسخگوست (no ZWNJ in «پاسخگو») |
| موفقیت! (alone) | انجام شد / ذخیره شد («با موفقیت ثبت شد» is common and fine) |
| چیزی برای نمایش وجود ندارد | هنوز چیزی ثبت نشده |
| به جامعهٔ ما بپیوندید | عضو … شوید |
| در پایان روز | در نهایت / آخرش |
| قدرت‌گرفته از X | بر پایهٔ X / با فناوری X |
| سفر شما با X | (drop it; say directly what happens) |
| تجربهٔ کاربری بی‌نظیر | (drop it) |
| هرگونه سؤال | سؤالی |
| به نظر می‌رسد که | (drop it) |
| بدون هیچ‌گونه | بدون |
| ما معتقدیم که / ما باور داریم که | (drop it; state the claim directly) |

**16. Imperative + reason in one sentence.** English says "Check your inbox, the link is there": it gives the user a task first, then the reason. Persian states the result and lets the reader figure out what to do.
❌ ایمیل‌تان را ببینید، لینک تأیید آن‌جاست.
✅ لینک تأیید ایمیل شد.
❌ به تنظیمات بروید، گزینهٔ خروج آن‌جاست.
✅ گزینهٔ خروج در تنظیمات است.

**17. Comma splice.** A comma doesn't join two independent sentences. Either use a period, connect with «و»/«که»/«تا», or drop one clause (pattern 16).
❌ پرداخت انجام نشد، دوباره امتحان کنید.
✅ پرداخت انجام نشد. دوباره امتحان کنید.

**18. Parenthetical adverb between two commas.** «به سوال مشتری، حتی نصف‌شب، جواب می‌دهد» splits the sentence in the middle. Persian puts the adverb at the start of the sentence or next to the verb.
❌ به سوال مشتری، حتی نصف‌شب، جواب می‌دهد.
✅ حتی نصف‌شب هم جواب مشتری را می‌دهد.

**19. Subjectless verb tricolon.** Three parallel clauses — "…does X, writes Y, and answers Z" — with no subject is an English advertising tricolon. Bring in the subject and break the rhythm: two clauses plus a separate sentence, or the subject up front with «هم» in the third clause.
❌ قیمت‌ها را هماهنگ می‌کند، توضیحات را می‌نویسد و به مشتری جواب می‌دهد.
✅ آکسون قیمت‌ها را هماهنگ می‌کند و توضیح محصول‌ها را می‌نویسد. جواب مشتری را هم خودش می‌دهد.

**20. Closing "you just …" punchline.** After a list of what a product does, a short second-person closer («شما فقط گزارشش را می‌بینید.») is a calque of "You just …". Persian states the outcome for the reader, not the reader as the subject of one small action.
❌ شما فقط گزارشش را می‌بینید.
✅ کار شما فقط دیدن گزارش است. / برای شما فقط گزارش می‌ماند.

**21. Coined word instead of an established loanword.** «برنامهٔ وب», «خوراک», «پاورقی سایت», «تصویر صفحه» where everyone actually says «وب‌اپلیکیشن», «فید», «فوتر», «اسکرین‌شات». List in `references/terms.md` and the domain files under `references/terms/`. The reverse is also wrong: don't turn «ایمیل» into «رایانامه».

**22. Clichéd essay-style opening.** «در دنیای امروز، X اهمیت زیادی دارد», «در عصر دیجیتال، X ضروری است», «در این مقاله/متن به بررسی … می‌پردازیم». These are the opening of a translated English essay. Persian starts directly with a claim or a question, not with throat-clearing about "today's world."
❌ در دنیای امروز، رقابت در فروشگاه‌های آنلاین بسیار زیاد شده است. در این مقاله به بررسی روش‌های افزایش فروش می‌پردازیم.
✅ رقابت در فروشگاه‌های آنلاین هر روز بیشتر می‌شود؛ این چند روش فروش را بالا می‌برد.

**23. Translated marketing or how-to heading.** «چرا باید X را انتخاب کنید؟», «مزایای استفاده از X», «X: راهنمای کامل». These are English landing-page/article heading templates, not what a real Persian site titles. Like pattern 12, report heading/caption changes separately under step 8 of editing mode and default to ⚠️, not an automatic ✅.
❌ چرا باید رصدبان را انتخاب کنید؟
✅ رصدبان چه فرقی با رصد دستی قیمت دارد؟

## Fixed mechanics

1. **ZWNJ (half-space):** «می‌شود», «نمی‌تواند», «کتاب‌ها», «به‌روزرسانی». Never «می شود» or «میشود».
2. **Persian letterforms, not Arabic:** «ی» and «ک», not «ي» and «ك».
3. **Persian digits** in running text (۱۲۳). Latin digits only inside code, IDs, version numbers and URLs. Thousands separator «٬» for five-digit numbers and up (۱۲٬۵۰۰); four-digit numbers get no separator (۱۴۰۵). Percent sign «٪» attached to the number. The project's existing style wins if there's a conflict.
4. **Ezafe mark after a silent «ه»:** default to «ٔ» (صفحهٔ اصلی, هزینهٔ پایه). If the project already writes «صفحه‌ی اصلی», keep that instead. Pick one per project.
5. **Persian punctuation:** «،» «؟» and «…» quotes. Not English comma/question mark, not " ". Exclamation marks only in friendly and casual tone, and sparingly even there.
6. **Semicolon «؛» only in formal tone.** In semi-formal, friendly and casual, use a period instead and split the sentence, or stitch it with «و». Text with a semicolon in every paragraph reads as machine-written.
7. **Never a comma before «و» or «یا».** «الف، ب، و پ» and «… می‌دهد، و هر معادل …» are calques of the Oxford comma. Either «الف، ب و پ» or a period and a new sentence. This rule is absolute.
8. **Keep tone consistent across the whole text;** don't drift between «می‌توانید» and «می‌تونید» on the same page.
9. **Bring the verb forward** if the sentence runs long; a Persian sentence with its verb thirty words away doesn't read.

## Writing mode

1. Settle the tone.
2. Before writing, **say the point of each paragraph as one spoken line** (in your head, not in the output): "I want to say this tool checks competitor prices every day and tells you if someone gets cheaper." Then write that same thought in the chosen tone. Don't translate from the English in your head.
3. Check `references/terms.md` and the relevant domain file(s) under `references/terms/` for terminology.
4. Pass the draft sentence by sentence through patterns 1–23. Rewrite any sentence that matches one, then pass the rewrite through the same list again.
5. Final test: read the text aloud; can you guess the English behind it? If yes, redo it. If the text is longer than a few sentences, also check it against "Structural tells of machine generation" below (decorative emoji, overused bold, artificial headings, clichéd closing).
6. Before presenting the final draft, pipe it through `python3 scripts/lint.py -` (stdin). Do this even when the text is only going into the chat, not a file — the `PostToolUse` hook only fires on `Write`/`Edit`, so plain chat output needs this manual pass to get the same mechanical check. Look at every hit; the report is a prompt to judge, not a verdict.

## Editing mode

0. First state which version of the skill you're working from (the `version` field in `.claude-plugin/plugin.json`, or if that file is missing, the version named at the top of `README.md`) so the user knows which rules applied.

1. **Clarify scope:** the team's own copy (headings, buttons, messages, meta, aria-labels, descriptions) is in scope; user-submitted content, data, quotes and brand names are out of scope unless the user says otherwise. List site-wide shared copy (header, footer) separately and ask about it.
2. Pass every sentence through patterns 1–23 and the fixed-mechanics rules, and if the text is more than a couple of paragraphs, also pass the whole document through "Structural tells of machine generation." **Pass every rewrite through the same list again too**; removing one pattern shouldn't introduce another (e.g. dropping «توسط» and ending up with an ezafe chain). If the new sentence isn't better than the original, leave it and move it to ⚠️. **Judge the text, not its author:** that a sentence was already reviewed, is live on the site, or is even one of this skill's own ✅ examples is not proof it's correct.
3. Output is always three-tier:
   - ✅ **Definite, applied:** table of before → after → which pattern.
   - ⚠️ **Possible, not applied:** table of text → location → the doubt → a suggestion. Anything you're unsure about goes here, not into silence. "When in doubt, report it," not "when in doubt, leave it."
   - ⏭ **Out of scope, not reviewed:** a short list (user data, header/footer, …) so the user knows what wasn't looked at.
4. A subjectless passive in formal tone, an established loanword, and deliberately translated examples (like the ❌ column of a comparison page) are not errors; if they look like a mistake at first glance, put them in ⚠️ and say why they were rejected.
5. Run `scripts/lint.py` on the text files (`python3 scripts/lint.py path…`). Its output is mechanical signals (ZWNJ, Arabic letters, Latin digits, «توسط», calques) plus matches against the full term glossary. Weigh every hit by eye; the lint report itself isn't the decision.
6. Don't commit anything unless the user asks.
7. **A tone change isn't a full rewrite.** When the user wants a new tone, only change sentences that don't fit the target tone, and write exactly what changed about the tone (verb form, spacing, address) in the "pattern" column. "Tone" alone isn't a sufficient label. Adding a pronoun is not a tone change (`references/tones.md`, "semi-formal → friendly" section).
8. **Report headings and captions separately.** A change to a heading, tagline, caption or label defaults to ⚠️, not ✅, unless it's an obvious calque (patterns 12 and 15). These are advertising copy and their terseness is deliberate.
9. **Two passes, maximum.** First pass: the original text. Second pass: only the sentences you yourself wrote. If the second pass still finds something in your own rewrites, apply it and stop. A third pass only produces ⚠️, never ✅. Endless editing doesn't improve text, it just keeps changing it.
10. **Write your own report under the same rules.** No «—», no «؛» (the report is semi-formal), no comma before «و». A report that's itself translated-sounding has no credibility.

## Structural tells of machine generation (document level)

Patterns 1–23 are all **sentence**-level. The four tells below are **document**-level, and they give away that a text is AI-written faster than the sentences themselves do, especially in longer text (a full landing page, an "about us" page, a blog post). Check for these in both writing mode (step 5) and editing mode, separately from running the sentence-level list:

- **Decorative emoji before every bullet** (🚀 fast, ✅ secure, 💡 smart). A Persian bullet either has no marker or uses «-»/«•»; an emoji before every line is English LinkedIn-post rhythm, not Persian prose. (This skill's own ✅/❌/⚠️/⏭ markers are an exception — they're for its own reports, not for final copy.)
- **Excessive bolding of random phrases** in a paragraph (every sentence has a bolded chunk). This pulls the reader off the sentence's line of thought and isn't common in Persian writing.
- **Artificial heading structure for short text** (splitting three lines into three separate headings). If the text is one short paragraph, leave it as one paragraph.
- **Clichéd closing "در پایان"/"جمع‌بندی"** in a text that doesn't need a summary at all (it's short, or it already stated the conclusion).

Test: if you removed the decoration, would the text lose anything? If not, it was excess decoration and should come out.

## What not to change

- Brand and product names, established legal and technical terminology, text the user wrote themselves, user-submitted content.
- A word that means something else in your sentence, just because it's in `terms.md` or a domain file. Every glossary row reports one context, not a universal rule. Never do a blind global find-and-replace.

## Help improve Hamghalam

If you spot a new translation-tell pattern that isn't in the list above, or a term models keep getting wrong, suggest the user register it at https://barchin.net/hamghalam. A report like "this sentence is translated because …" is worth more than a bare pair of phrases.
