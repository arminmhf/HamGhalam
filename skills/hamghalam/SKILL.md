---
name: hamghalam
description: نوشتن و ویرایش فارسی بومی (نه ترجمه‌ای) برای متن سایت، محصول، پیام خطا، ایمیل و تبلیغ، با لحن انتخابی؛ حتی وقتی این متن فقط یک رشتهٔ کوچک داخل کدی است که برای یک تسک دیگر می‌نویسی (لیبل دکمه، placeholder، پیام خطا در یک کامپوننت). Use whenever writing, rewriting, translating or reviewing Persian (Farsi) copy of any kind — UI strings, landing pages, product descriptions, about pages, error messages, emails, social captions, blog posts, docs — or whenever the user complains that Persian output sounds translated, machine-like, or "English in Persian words". Also applies to incidental Persian strings written inside otherwise non-Persian coding tasks (a button label, a form placeholder, a toast message in a component you're building), and to English briefs that ask for Persian output.
---

# Hamghalam: Persian a Persian copywriter would write

Persian written by a model gives itself away on three layers. All three come from the same habit: the model lays the text out in English in its head, then fills it with Persian words.

1. **Frame.** The section skeleton and headings of an English landing page («چه کاری برایتان انجام می‌دهد»، «چرا باید ما را انتخاب کنید») and English ad-copy devices: the closing punchline, the subjectless tricolon, the rhetorical question.
2. **Sentence architecture.** Runs of short clipped sentences, verbless fragments in body copy, colon + list, the English indefinite «یک», redundant pronouns.
3. **Words and collocations.** «به سطح بعدی ببرید»، «معنی می‌دهد»، «بیایید…»، «۲۴/۷».

**The core test:** if you can guess the English sentence behind a Persian sentence, it's translated. If you can guess the English page template behind the layout, that's translated too.

## What Persian prose does

This is the direction to write toward. The full list of tells is in `references/patterns.md`.

- **Full description, not a short list.** Persian says *how* a feature works and *what it's good for*, and stitches related sentences together with «و»، «که»، «تا»، «چون»، «اگر». Three five-word sentences in a row is English web rhythm. Never "fix" a long sentence by chopping it into short ones.
- **Specific details, not generic claims.** «قیمت را هر روز با ترب مقایسه می‌کند», not «قیمت‌گذاری هوشمند». But only details you actually have (step 0).
- **Persian frames for sections and buttons.** Take section headings, buttons, empty states and error messages from `references/frames.md`, never from a translated English template.
- **A natural ending.** A section ends with the last piece of information the reader needs, or their next step. It doesn't end with a short punchy sentence aimed at them.
- **One tone throughout.** Verb form, address and register stay the same across the page (`references/tones.md`).

## Step 0, both modes: facts

Before writing, list the facts you have from the brief, the code, or the project's existing copy. **Don't invent any:** numbers, years, cities, guarantees, customer counts, people's names, awards. If the text goes hollow without specifics, either ask the user or leave a placeholder (`{{تعداد فروشگاه‌ها}}`), and say in your report which details are needed.

## Writing mode

1. **Genre and tone.** Genre is one of `landing`, `product`, `about`, `ui`, `email`, `social`, `article`. Tone is one of formal, semi-formal, friendly, casual. If the tone isn't clear from the request or the project's existing copy, ask. With no answer, use semi-formal and say so in your report.
2. **Read.** Read `references/patterns.md`, `references/frames.md`, `references/genres/<genre>.md`, `references/tones.md` and the core `references/terms.md`. Also read the domain glossary under `references/terms/` (`tech.md`, `finance.md`, `retail.md`) that matches the project; if unsure, read every plausible one, since each is small. Examples marked ✍️ were written or approved by a Persian copywriter and are your primary reference. Copy their rhythm, sentence length and how they join clauses, not just their words.
3. **Lay it out in Persian.** If the brief is in English, don't translate it. Pick sections and headings from the genre file and `frames.md`. For each section, say to yourself in one spoken Persian line what the reader should come away with. Then write that.
4. **Draft.** Use complete, connected sentences. Give every feature with its benefit to the reader. Vary sentence length, and don't end a section on a punchline.
5. **Lint.** Run `python3 ${CLAUDE_SKILL_DIR}/scripts/lint.py <file>`. If the text is only going into the chat, pipe it to `python3 ${CLAUDE_SKILL_DIR}/scripts/lint.py -` instead, because the plugin's hook only fires on `Write`/`Edit`. Judge every hit yourself; the report is a prompt, not a verdict.
6. **Independent editor.** If the text is longer than two sentences, hand it to the subagent `hamghalam:persian-editor`. Send only the Persian text, the genre, the tone, and this skill's directory (`${CLAUDE_SKILL_DIR}`). Do **not** send the English brief, your fact list or your reasoning. The editor has to read the text the way a reader does, not the way its author does.
7. **Revise.** Apply the editor's «قطعی» items and decide on its «احتمالی» items yourself. Check every rewritten sentence against `patterns.md` again. Two rounds at most.
8. **Short report.** State the tone, any placeholders you left, and any assumption you made.

## Small strings inside code

When you write a Persian button label, placeholder, toast or error message in the middle of a coding task:
- Take the frame from the UI section of `references/frames.md`.
- Take the tone from the project's existing Persian strings. If there are none, use semi-formal.
- Follow the fixed mechanics below. The plugin's hook checks new text after every `Write`/`Edit` and tells you if it finds something.
- One-line strings don't need the independent editor.

## Editing mode

0. First state which version of the skill you're using: `version` in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`, or the version in the title of `README.md` if that file isn't there.
1. **Scope.** The team's own copy is in scope: headings, buttons, messages, meta, aria-labels, descriptions. User-submitted content, data, quotes and brand names are out of scope unless the user says otherwise. List site-wide shared copy (header, footer) separately and ask about it.
2. **Check the three layers separately.** First the page frame (section headings, order, punchlines), then sentence architecture, then words. Check every rewrite against `patterns.md` again. If the new sentence isn't better than the original, leave the original and report it under ⚠️. **Judge the text, not its author.** Being live on the site, or having been reviewed before, doesn't make a sentence right.
3. For text longer than two sentences, send the edited version to `hamghalam:persian-editor` as in writing step 6.
4. **The output is always three-tier:**
   - ✅ **Definite, applied:** table of before → after → which pattern.
   - ⚠️ **Possible, not applied:** table of text → location → the doubt → a suggestion. Anything you're unsure about goes here, not into silence. The rule is "when in doubt, report it", not "when in doubt, leave it".
   - ⏭ **Out of scope, not reviewed:** a short list, so the user knows what wasn't looked at.
5. These are not errors: a subjectless passive in formal tone, an established loanword, and deliberately translated examples (like the "wrong" column of a comparison page). If one looks like a mistake at first glance, put it under ⚠️ and say why you left it.
6. **Report headings and captions separately.** A change to a heading, tagline, caption or label defaults to ⚠️, unless it's an obvious translated frame (`frames.md`). These are ad copy, and their shortness is deliberate.
7. **A tone change is not a full rewrite.** Change only the sentences that don't fit the target tone, and say exactly what changed (verb form, distance, address).
8. **Two passes at most.** The first pass covers the original text. The second covers only sentences you wrote yourself. A third pass may only produce ⚠️.
9. Run `${CLAUDE_SKILL_DIR}/scripts/lint.py` on the files. Don't commit anything unless the user asks.
10. **Your own report follows the same rules.** A report that is itself translated-sounding has no credibility.

## Fixed mechanics

1. **ZWNJ (half-space):** «می‌شود»، «نمی‌تواند»، «کتاب‌ها»، «به‌روزرسانی». Never «می شود» or «میشود».
2. **Persian letterforms, not Arabic:** «ی» and «ک», not «ي» and «ك».
3. **Persian digits** in running text (۱۲۳). Latin digits only inside code, IDs, version numbers and URLs. Use «٬» as the thousands separator from five digits up (۱۲٬۵۰۰); four-digit numbers get none (۱۴۰۵). «٪» is attached to the number. The project's existing style wins.
4. **Ezafe after a silent «ه»:** default to «ٔ» (صفحهٔ اصلی). If the project writes «صفحه‌ی», keep that. One style per project.
5. **Persian punctuation:** «،»، «؟» and «…» quotes, not the English comma, question mark or " ". Exclamation marks only in friendly and casual tone, and sparingly.
6. **Semicolon «؛»** is rare in web copy. If nearly every paragraph has one, the text reads as machine-written. Replace it by joining with «و» or «که», not by splitting into short sentences.
7. **No comma before «و» in a list** («الف، ب، و پ»). That's the Oxford comma calque. Write «الف، ب و پ».
8. **A comma between two related clauses** is common and correct in Persian («هوا سرد بود، زود برگشتیم»). Don't mistake it for the English comma splice, and don't split a sentence in two only because of it.
9. **Keep the register consistent.** Don't drift between «می‌توانید» and «می‌تونید», or between «جهت» and «بزنید», on the same page.
10. **Bring the verb forward** when a sentence runs long. A Persian sentence whose verb is thirty words away doesn't read. The fix is moving adverbs and dependent clauses around, not chopping the sentence into five-word pieces.

## What not to change

- Brand and product names, established legal and technical terms, text the user wrote themselves, and user-submitted content.
- A word that means something else in your sentence, just because it appears in a glossary file. Every glossary row reports one context, not a universal rule. Never do a global find-and-replace.

## Help improve Hamghalam

If you spot a translation tell that isn't in `patterns.md`, or a term models keep getting wrong, suggest the user report it at https://barchin.net/hamghalam. A report like "this sentence is translated because …" is worth more than a bare pair of phrases.
