---
name: hamghalam
description: نوشتن و ویرایش فارسی بومی (نه ترجمه‌ای) برای متن سایت، محصول، پیام خطا، ایمیل و تبلیغ، با لحن انتخابی؛ حتی وقتی این متن فقط یک رشتهٔ کوچک داخل کدی است که برای یک تسک دیگر می‌نویسی (لیبل دکمه، placeholder، پیام خطا در یک کامپوننت). Use whenever writing, rewriting, translating or reviewing Persian (Farsi) copy of any kind — UI strings, landing pages, product descriptions, about pages, error messages, emails, social captions, blog posts, docs — or whenever the user complains that Persian output sounds translated, machine-like, or "English in Persian words". Also applies to incidental Persian strings written inside otherwise non-Persian coding tasks (a button label, a form placeholder, a toast message in a component you're building), and to English briefs that ask for Persian output.
---

# Hamghalam: Persian a Persian copywriter would write

Model-written Persian gives itself away in a few specific ways, and a Persian copywriter reviewed every rule in this skill (✍️ in the reference files). Three things came out of that review:

1. **The real tells are narrower than they look.** They are short clipped sentences, implied nouns and vague verbs, translated section frames and buttons, a handful of collocations («به سطح بعدی ببرید»، «هیجان‌زده‌ایم»), and spoken idioms in semi-formal copy.
2. **Over-correcting is a tell too.** Many constructions that resemble English are ordinary Persian: «توسط», rhetorical questions, colon lists, «نه تنها … بلکه», verbless fragments. Rewriting them, or making semi-formal copy chatty to sound "less translated", produced text the copywriter rejected. `references/patterns.md` section D lists what not to touch.
3. **This skill removes translation tells, never the marketing.** ✍️ «پلاگین نباید جلوی موارد مارکتینگی را بگیرد.» In blind tests the copywriter preferred plain model output for product descriptions, about pages and emails whenever this skill had made them dry. Persian copy sells, has feeling, tells a small story and greets warmly.

**The core test:** would a Persian copywriter have written this sentence, with these words, on this kind of page? If you can guess the English sentence or the English page template behind it, they wouldn't.

## What Persian copy does

- **It says everything in full.** It names the noun instead of leaving it implied («مشخصات محصول», not «مشخصات»; «با همین موارد», not «با همین»). It uses the precise verb («استخراج می‌کند و در وب‌سایت شما اعمال می‌کند», not «از کاتالوگ می‌نویسد»). Sentences run longer than English ones: «در فارسی ما بیشتر توضیح می‌دهیم» ✍️.
- **Semi-formal means written Persian.** Use «اطلاع می‌دهیم»، «ارسال می‌شود»، «مراقب … است»، «شما را در جریان امور قرار می‌دهد». Don't use spoken idioms («خبرتان می‌کنیم»، «جلویتان می‌گذارد»، «حواسش هست»، «درست‌وحسابی»), which belong to friendly and casual tone. This was the copywriter's main complaint.
- **Short forms are Persian forms.** A verbless feature line («نصب سریع، حجم کم همراه با آپدیت خودکار.» ✍️), a verbless status («پرداخت ناموفق.» ✍️), a short question in product copy («عجله دارید؟ معطلتان نمی‌کند.» ✍️) are all fine. Several short *complete verb sentences* stacked as body description are not.
- **It sells, warmly.** ✍️ Benefit framing («انتخابی هوشمندانه برای کسانی است که …»), feeling, a short story on an about page, and warm openings and sign-offs in friendly email («سلام دوست عزیز،»، «خبر خوب!»، «با مهر،») are all Persian copy. Don't trade them for a dry list of specs. The only imagery to avoid is the translated kind («کرمای طلایی» ✍️).
- **Persian frames.** Section headings, buttons and fixed messages come from `references/frames.md`.
- **A full closing line.** Don't end on a terse «شما فقط … می‌بینید».

## Step 0, both modes: facts

Before writing, list the facts you have from the brief, the code, or the project's existing copy. **Don't invent hard facts:** numbers, years, cities, guarantees, customer counts, people's names, awards. Feeling, benefit framing and atmosphere are not facts; write them freely. If the text goes hollow without specifics, either ask the user or leave a placeholder (`{{تعداد فروشگاه‌ها}}`), and say in your report which details are needed.

## Writing mode

1. **Genre and tone.** Genre is one of `landing`, `product`, `about`, `ui`, `email`, `social`, `article`. Tone is one of formal, semi-formal, friendly, casual. If the tone isn't clear from the request or the project's existing copy, ask. With no answer, use semi-formal and say so in your report.
2. **Read.** Read `references/patterns.md`, `references/frames.md`, `references/genres/<genre>.md`, `references/tones.md` and the core `references/terms.md`. Also read the domain glossary under `references/terms/` (`tech.md`, `finance.md`, `retail.md`) that matches the project; if unsure, read every plausible one, since each is small. The ✍️ examples in the genre file are your primary reference for register, sentence length and how clauses join. **Never copy their sentences or details** (products, cities, steps such as «موکاپات»); they describe other businesses, and copying them invents facts about yours.
3. **Lay it out in Persian.** If the brief is in English, don't translate it. Pick sections and headings from the genre file and `frames.md`. For each section, say to yourself in one Persian line what the reader should come away with. Then write that.
4. **Draft.** Use written Persian for semi-formal and formal tone. Name every noun and use precise verbs. Join related clauses with «و»، «که»، «تا» or a comma, and vary how you join them.
5. **Lint.** Run `python3 ${CLAUDE_SKILL_DIR}/scripts/lint.py --tone <tone> <file>`, with the tone as `formal`, `semi_formal`, `friendly` or `casual`. If the text is only going into the chat, pipe it to `python3 ${CLAUDE_SKILL_DIR}/scripts/lint.py --tone <tone> -` instead, because the plugin's hook only fires on `Write`/`Edit`. Judge every hit yourself; the report is a prompt, not a verdict.
6. **Independent editor.** If the text is longer than two sentences, hand it to the subagent `hamghalam:persian-editor`. Send only the Persian text, the genre, the tone, and this skill's directory (`${CLAUDE_SKILL_DIR}`). Do **not** send the English brief, your fact list or your reasoning. The editor has to read the text the way a reader does, not the way its author does.
7. **Revise.** Apply the editor's «قطعی» items and decide on its «احتمالی» items yourself. Check every rewritten sentence against `patterns.md` again, including section D. Two rounds at most.
8. **Short report.** State the tone, any placeholders you left, and any assumption you made.

## Small strings inside code

When you write a Persian button label, placeholder, toast or error message in the middle of a coding task:
- Use the UI section of `references/frames.md` first; many common messages are there verbatim.
- Take the tone from the project's existing Persian strings. If there are none, use semi-formal.
- Follow the fixed mechanics below. The plugin's hook checks new text after every `Write`/`Edit` and tells you if it finds something.
- One-line strings don't need the independent editor.

## Editing mode

0. First state which version of the skill you're using: `version` in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`, or the version in the title of `README.md` if that file isn't there.
1. **Scope.** The team's own copy is in scope: headings, buttons, messages, meta, aria-labels, descriptions. User-submitted content, data, quotes and brand names are out of scope unless the user says otherwise. List site-wide shared copy (header, footer) separately and ask about it.
2. **Change only real tells.** Check frames first, then register, then sentences, then words. A sentence that only matches something in `patterns.md` section D is not an error, so leave it alone. Check every rewrite against `patterns.md` again. If the new sentence isn't clearly better than the original, keep the original and report it under ⚠️. **Judge the text, not its author.** Being live on the site, or having been reviewed before, doesn't make a sentence right.
3. For text longer than two sentences, send the edited version to `hamghalam:persian-editor` as in writing step 6.
4. **The output is always three-tier:**
   - ✅ **Definite, applied:** table of before → after → which pattern.
   - ⚠️ **Possible, not applied:** table of text → location → the doubt → a suggestion. Anything you're unsure about goes here, not into silence.
   - ⏭ **Out of scope, not reviewed:** a short list, so the user knows what wasn't looked at.
5. **Report headings and captions separately.** A change to a heading, tagline, caption or label defaults to ⚠️, unless the heading is in the «نه» column of `frames.md`.
6. **A tone change is not a full rewrite.** Change only the sentences that don't fit the target tone, and say exactly what changed (verb form, distance, address).
7. **Two passes at most.** The first pass covers the original text. The second covers only sentences you wrote yourself. A third pass may only produce ⚠️.
8. Run `${CLAUDE_SKILL_DIR}/scripts/lint.py --tone <tone>` on the files. Don't commit anything unless the user asks.
9. **Your own report follows the same rules.** A report that is itself translated-sounding has no credibility.

## Fixed mechanics

1. **ZWNJ (half-space):** «می‌شود»، «نمی‌تواند»، «کتاب‌ها»، «به‌روزرسانی». Never «می شود» or «میشود».
2. **Persian letterforms, not Arabic:** «ی» and «ک», not «ي» and «ك».
3. **Persian digits** in running text (۱۲۳). Latin digits only inside code, IDs, version numbers and URLs. Use «٬» as the thousands separator from five digits up (۱۲٬۵۰۰); four-digit numbers get none (۱۴۰۵). «٪» is attached to the number. The project's existing style wins.
4. **Ezafe after a silent «ه»:** default to «ٔ» (صفحهٔ اصلی). If the project writes «صفحه‌ی», keep that. One style per project.
5. **Persian punctuation:** «،»، «؟» and «…» quotes, not the English comma, question mark or " ".
6. **Never a comma before «و» or «که»** ✍️.
7. **A comma between two related clauses is fine** ✍️ («قیمت رقبا هر روز تغییر می‌کنند، آکسون قیمت‌ها را …»). Don't split such a sentence in two.
8. **«؛»** sparingly in formal and semi-formal tone ✍️, never in every paragraph, and not in friendly or casual tone.
9. **Exclamation marks:** none in formal or semi-formal. In friendly tone, in one or two messages, not all ✍️.
10. **One register per page.** Don't drift between «می‌توانید» and «می‌تونید», or between written and spoken verbs.

## What not to change

- Brand and product names, established legal and technical terms, text the user wrote themselves, and user-submitted content.
- Anything listed in `patterns.md` section D.
- A word that means something else in your sentence, just because it appears in a glossary file. Every glossary row reports one context, not a universal rule. Never do a global find-and-replace.

## Help improve Hamghalam

If you spot a translation tell that isn't in `patterns.md`, or a term models keep getting wrong, suggest the user report it at https://barchin.net/hamghalam. A report like "this sentence is translated because …" is worth more than a bare pair of phrases.
