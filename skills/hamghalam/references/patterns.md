# Translation tells

Each tell has a pair of examples. ❌ is a sample of the mistake, not text to imitate. ✅ shows the direction.
✍️ marks an example written or approved by a Persian copywriter. Unmarked examples were written by a model and only show the direction.
`[rule]` is the matching rule id in `scripts/lint.py`.

## A. Frame and document

These give the text away before any single sentence does, because the reader sees the shape of the page before reading it.

**A1. Translated section heading.** «چه کاری برایتان انجام می‌دهد»، «چرا باید X را انتخاب کنید؟»، «آماده‌اید شروع کنید؟»، «مشتریان دربارهٔ ما چه می‌گویند». Persian equivalents are in `frames.md`. `[cliche_heading]`

**A2. Closing punchline.** After a list of what the product does, a short second-person line that delivers the payoff like a slogan ("You just …"). Changing the words («سهم شما فقط…»، «کار شما فقط…») keeps the device. End on the last piece of information the reader needs, or fold the payoff into the previous sentence. `[you_just]` `[punchline_only]`
❌ قیمت‌ها را هماهنگ می‌کند، توضیح محصول می‌نویسد و به مشتری جواب می‌دهد. شما فقط گزارشش را می‌بینید.
✅ (waiting for the copywriter's example)

**A3. Subjectless verb tricolon.** Three parallel clauses «… می‌کند، … می‌نویسد و … می‌دهد» is English ad rhythm. Give each feature its own sentence with its benefit. Reordering the clauses, or splitting them into shorter sentences, doesn't fix it. `[tricolon]`

**A4. Essay-style opening.** «در دنیای امروز…»، «در عصر دیجیتال…»، «در این مقاله به بررسی … می‌پردازیم». Start directly with the claim or the reader's problem. `[essay_opener]`
❌ در دنیای امروز، رقابت در فروشگاه‌های آنلاین بسیار زیاد شده است. در این مقاله به بررسی روش‌های افزایش فروش می‌پردازیم.
✅ رقابت بین فروشگاه‌های آنلاین هر روز سخت‌تر می‌شود. در ادامه چند راه ساده را مرور می‌کنیم که به فروش بیشتر کمک می‌کند.

**A5. About page opening with «ما یک … هستیم».** Calque of "We are a …". Start with the work, the place or the story. `[we_are_a]`
❌ ما یک برشته‌کاری کوچک در شیراز هستیم.

**A6. Rhetorical question or throat-clearing.** «آیا تا به حال…؟»، «آماده‌اید؟»، «تصور کنید…». Start with the point itself. `[rhetorical_q]`
❌ آیا تا به حال به این فکر کرده‌اید که چطور می‌توانید قیمت رقبا را رصد کنید؟
✅ رصد دستی قیمت رقبا وقت زیادی می‌گیرد و همیشه هم دقیق نیست.

**A7. Generic claims, or invented details.** «کسب‌وکارتان را متحول می‌کند» with no number, time, place or guarantee is hollow. Invented details are worse. Use only details from the brief or the project, and leave placeholders for the rest.

**A8. Uniform symmetry.** Every card or paragraph has the same length and shape (a two-word heading and two equal sentences). Human prose runs longer where there's more to say.

**A9. Document decoration.** The linter reports these as `[D]`:
- an emoji before every bullet
- a bolded chunk in every sentence
- three headings over what is really one paragraph
- «جمع‌بندی» or «در پایان» on a short text

Test: does the text lose anything if you remove the decoration?

## B. Sentence architecture

**B1. Runs of short clipped sentences.** This is what a Persian reader notices first. Three five-word sentences in a row is English web rhythm. Persian stitches related sentences together with «و»، «که»، «تا»، «چون» and commas, and explains. `[staccato]`
❌ سریع نصب می‌شود. حجمش کم است. آپدیت خودکار دارد.
✅ (waiting for the copywriter's example)

**B2. Verbless fragments in body copy.** A noun phrase punctuated like a sentence. Headlines, taglines, captions, labels and card titles are verbless in Persian too and shouldn't get a forced verb. What's wrong even in a headline is a string of one-word fragments with periods («سریع. امن. ساده.»).
❌ سریع. امن. بدون دردسر.
✅ (waiting for the copywriter's approval)

**B3. Colon + list of noun phrases** in body copy ("X: a, b, and c"). Say it as a full sentence. `[colon_list]`
❌ سه مزیت دارد: سرعت بالا، نصب آسان و پشتیبانی ۲۴ ساعته.
✅ سریع است، راحت نصب می‌شود و پشتیبانی‌اش هم شبانه‌روزی است.

**B4. English-style indefinite «یک».** Translating "a/an" as «یک». Persian more often uses the «ی» suffix, or nothing. `[indef_yek]`
❌ آکسون یک دستیار هوشمند است که قیمت‌ها را به‌روز نگه می‌دارد.
✅ آکسون دستیار هوشمندی است که قیمت‌ها را به‌روز نگه می‌دارد.

**B5. Passive with «توسط».** The subject is known, so make the sentence active. A subjectless passive («لینک فرستاده شد») is natural. `[tavassot]`
❌ این گزارش توسط تیم پشتیبانی بررسی می‌شود.
✅ تیم پشتیبانی این گزارش را بررسی می‌کند.

**B6. Nominalization.** «انجام X»، «اقدام به X»، «مورد X قرار گرفتن» instead of a plain verb. `[nominal]`
❌ برای انجام ثبت‌نام، اقدام به وارد کردن شماره تلفن کنید.
✅ برای ثبت‌نام، شماره تلفنتان را وارد کنید.

**B7. «به شما اجازه می‌دهد تا» and «کمک می‌کند تا».** Make the user the subject, or bring the tool in with «با». `[allows_you]`
❌ این ابزار به شما اجازه می‌دهد تا گزارش‌ها را دانلود کنید.
✅ با این ابزار می‌توانید گزارش‌ها را دانلود کنید.

**B8. Redundant pronouns.** «شما»، «خود»، «آن» where Persian drops the pronoun or uses an attached one. `[pronoun_khod]`
❌ شما می‌توانید تنظیمات خود را در پنل کاربری خود تغییر دهید.
✅ تنظیمات حسابتان را از پنل کاربری می‌توانید تغییر دهید.

**B9. «نه تنها … بلکه» and «این فقط X نیست، Y است».** Persian says «هم … هم», or just says what the thing is. `[not_only]` `[not_just]`
❌ نه تنها سریع است، بلکه امن نیز هست. / این فقط یک ابزار نیست، یک دستیار واقعی است.
✅ هم سریع است، هم امن.

**B10. Cleft «این … است که».** Calque of "It's you who …". `[cleft]`
❌ این شما هستید که تصمیم نهایی را می‌گیرید.
✅ تصمیم نهایی با خودتان است.

**B11. Discourse marker opening consecutive sentences.** «همچنین،»، «علاوه بر این،»، «در نتیجه،»، «به عبارت دیگر،» (Moreover, Additionally). Join the sentence to the previous one, or drop the marker. `[discourse_marker]`

**B12. «اینجاست که…» and «این یعنی…».** Calques of "This is where … comes in" and "This means". `[this_is_where]` `[this_means]`

**B13. Sentence opening with «با استفاده از».** Calque of "Using …". Usually «با X» is enough. `[with_using]`

**B14. Ezafe chain.** Three ezafes in a row instead of a predicate or a preposition.
❌ عبارت‌های ترجمه‌ای متن‌های هوش مصنوعی را جمع می‌کند.
✅ عبارت‌های ترجمه‌ای را از متن‌های هوش مصنوعی جمع می‌کند.

**B15. Parenthetical em dash «—».** Use a comma, «که», or a separate sentence. `[em_dash]`
❌ رصدبان — ابزار پایش قیمت رقبا — رایگان شد.
✅ رصدبان که قیمت رقبا را پایش می‌کند، رایگان شد.

**B16. Adverb wedged between two commas.** «به سوال مشتری، حتی نصف‌شب، جواب می‌دهد» splits the sentence in the middle. Put the adverb at the start or next to the verb. `[parenthetical_adverb]`
❌ به سوال مشتری، حتی نصف‌شب، جواب می‌دهد.
✅ حتی نصف‌شب هم جواب مشتری را می‌دهد.

**B17. «در حال … هستید».** `[dar_hal_hastid]`
❌ شما در حال مشاهدهٔ نسخهٔ آزمایشی هستید.
✅ این نسخهٔ آزمایشی است.

## C. Words and phrases

**C1. Intensifiers.** واقعاً، به‌سادگی، به‌راحتی، به‌طور یکپارچه، به‌طور کامل، کاملاً، در واقع، بی‌نظیر. Drop most of them. `[intensifier]`
❌ به‌سادگی می‌توانید به‌طور یکپارچه با ابزارهای خود ادغام شوید.
✅ به ابزارهایی که همین حالا با آن‌ها کار می‌کنید وصل می‌شود.

**C2. Translated collocations.** A verb and noun that go together in English but not in Persian. `[calque]`

| Translated | Source | Write instead |
|---|---|---|
| معنی می‌دهد | makes sense | منطقی است / به کار می‌آید |
| تفاوت ایجاد کنید | make a difference | say the concrete result |
| زمانتان را ذخیره کنید | save time | وقتتان کمتر هدر می‌رود |
| به سطح بعدی ببرید | next level | say the concrete result |
| X را تجربه کنید | experience X | use a concrete verb |
| در قلب X | at the heart of | drop it, or say what's central |
| با ذهنی آسوده | peace of mind | با خیال راحت |
| مطمئن شوید که | make sure | حتماً … / دقت کنید که |
| هیجان‌زده‌ایم که | we're excited to | خوشحالیم / just give the news |
| یک کلیک و … | one click and … | با یک کلیک … |
| ما هستیم | we're here | به پشتیبانی بگویید |
| بیایید … | let's … | drop it; say it directly |
| ۲۴/۷ | 24/7 | شبانه‌روزی |

**C3. English marketing vocabulary.** «راه‌حل‌ها» (solutions)، «قدرتمند» (powerful)، «اکوسیستم»، «توانمندسازی». Say exactly what it does.

**C4. Calqued boilerplate.** Replace these unconditionally:

| Calque | Write instead |
|---|---|
| خوش برگشتید! | خوش آمدید / (drop it) |
| چیزی اشتباه پیش رفت | مشکلی پیش آمد |
| ما اینجا هستیم تا کمک کنیم | اگر مشکلی بود، به ما بگویید |
| موفقیت! (alone) | انجام شد / ذخیره شد |
| چیزی برای نمایش وجود ندارد | هنوز چیزی ثبت نشده |
| به جامعهٔ ما بپیوندید | عضو … شوید |
| در پایان روز | در نهایت / آخرش |
| قدرت‌گرفته از X | بر پایهٔ X / با فناوری X |
| سفر شما با X | (drop it; say what actually happens) |
| تجربهٔ کاربری بی‌نظیر | (drop it) |
| هرگونه سؤال | سؤالی |
| به نظر می‌رسد که | (drop it) |
| بدون هیچ‌گونه | بدون |
| ما معتقدیم که / ما باور داریم که | (drop it; state the claim) |

**C5. Coined word instead of an established loanword.** «برنامهٔ وب»، «خوراک»، «پاورقی سایت»، «تصویر صفحه» where everyone says «وب‌اپلیکیشن»، «فید»، «فوتر»، «اسکرین‌شات». The reverse is also wrong: don't turn «ایمیل» into «رایانامه». Lists in `terms.md` and `terms/`.

**C6. Mixed register.** A bureaucratic word next to a colloquial verb («جهت ثبت سفارش روی دکمه بزنید»), or «محصولات» and «محصول‌ها» in the same text. Pick one register.
