# Translation tells

✍️ marks a verdict or example from a Persian copywriter (the 2026-10-01 review). Unmarked items come from model output observed in evals and only show the direction.
❌ is a sample of the mistake, not text to imitate. `[rule]` is the matching rule id in `scripts/lint.py`.

Read section D as carefully as the rest. Over-correcting, i.e. rewriting normal Persian because it resembles English, produced odd "de-translated" Persian in earlier versions of this skill, and readers noticed that too.

## A. Frame and register

**A1. Spoken words in semi-formal copy.** ✍️ This was the copywriter's main reason for preferring plain model output over this skill's earlier output. Semi-formal web Persian is *written* Persian. Spoken idioms belong in friendly and casual tone only. `[spoken_register]`

| Spoken (too casual for semi-formal) | Written ✍️ |
|---|---|
| با پیامک خبرتان می‌کنیم | با پیامک اطلاع می‌دهیم |
| گزارش را جلویتان می‌گذارد | شما را در جریان امور قرار می‌دهد |
| حواسش به فروشگاهتان است | مراقب کارهای فروشگاهتان است |
| بسته‌ها به همهٔ شهرها می‌رود | بسته‌ها به همهٔ شهرها ارسال می‌شوند |
| این اطلاعات مستقیم به بانک می‌رسد | این اطلاعات مستقیم به بانک ارسال می‌شود |
| اسپرسوی درست‌وحسابی | اسپرسوی عالی |

**A2. Translated section heading or button.** ✍️ «X چه کاری برایتان انجام می‌دهد؟»، «X چه باری از دوشتان برمی‌دارد؟»، «آماده‌اید شروع کنید؟»، «مأموریت ما»، button «شروع کنید» or «بیشتر بدانید». The approved replacements are in `frames.md`. `[bad_frame]` `[bare_cta]`

**A3. Short closing line with the reader as subject.** ✍️ After a list of what the product does, a terse «شما فقط گزارشش را می‌بینید.» is a calque of "You just …". `[you_just]`
❌ قیمت‌ها را هماهنگ می‌کند، توضیحات را می‌نویسد و به مشتری جواب می‌دهد. شما فقط گزارشش را می‌بینید.
✅ ✍️ در نهایت برای تمام کارهای انجام‌شده، گزارشی را به شما ارائه می‌دهد.
✅ ✍️ برای تمام این موارد، سهم شما فقط مرور یک گزارش است.
These are two ways to close, not a template. Ending every section or every text with «در نهایت، …» is a formula of its own; most sections just end on their last piece of information. `[closing_formula]`

**A4. Invented hard facts.** Numbers, years, cities, guarantees, customer counts, names and awards come from the brief or the project, or stay as placeholders. This rule is about facts only. ✍️ Persuasive framing, feeling and atmosphere are not "generic claims" to strip out (section D).

**A5. Uniform symmetry and repeated joins.** Every card or paragraph the same length and shape, or a «برای همین …» / «پس …» clause hung on sentence after sentence. Vary the joins, and let some features stand without a stated benefit. `[connector_repeat]`
❌ پمپ ۱۵ باری دارد و فشارش کافی است. حدود ۴۰ ثانیه گرم می‌شود، برای همین لازم نیست منتظر بمانید. مخزنش جدا می‌شود، پس لازم نیست دستگاه را جابه‌جا کنید.

**A6. Document decoration.** These are reported by the linter as `[D]`:
- an emoji before every bullet
- a bolded chunk in every sentence
- three headings over what is really one paragraph
- «جمع‌بندی» on a short text

**A7. Fine once, a tell when repeated.** ✍️ Each of these is normal Persian on its own. Used twice or more in one text, they read as a model's habit. `[indef_yek]` `[we_are_a]` `[lets]` `[not_just]`
- «یک» as an indefinite article («آکسون یک دستیار هوشمند است»)
- «ما یک … هستیم» at the start of an about page
- «بیایید …»
- «این فقط X نیست، Y است»

## B. Sentence

**B1. Short complete sentences in a row.** ✍️ «جملات کوتاه تکه‌تکه‌شده مناسب نیست.» Several short *verb* sentences stacked as body description is English web rhythm. Persian does one of two things instead. It writes a full, connected description, or, for a quick feature summary, a verbless phrase list. `[staccato]`
❌ سریع نصب می‌شود. حجمش کم است. آپدیت خودکار دارد.
✅ ✍️ نصب سریع، حجم کم همراه با آپدیت خودکار.
❌ قیمت‌ها را با ترب و باسلام هماهنگ می‌کند، توضیحات محصول را از کاتالوگ سازنده می‌نویسد و به سوال مشتری، حتی نصف‌شب، جواب می‌دهد. شما فقط گزارشش را می‌بینید.
✅ ✍️ قیمت‌های وب‌سایت شما را با توجه به رقبایتان در ترب و باسلام مدیریت می‌کند، اطلاعات محصولات فروشگاهتان را از کاتالوگ سازنده استخراج می‌کند و در وب‌سایت شما اعمال می‌کند و به‌صورت شبانه‌روزی پاسخگوی مشتریان شما است. در نهایت برای تمام کارهای انجام‌شده، گزارشی را به شما ارائه می‌دهد.

**B2. Implied nouns.** ✍️ «در فارسی ما بیشتر توضیح می‌دهیم.» A model drops the noun that the previous sentence made "obvious". Persian names it.
❌ برای همین مشخصات دقیق است. ✅ ✍️ برای همین مشخصات محصول دقیق است.
❌ سفارشتان با همین ثبت می‌شود. ✅ ✍️ سفارشتان با همین موارد ثبت می‌شود.
❌ تا با هم انتخاب کنیم. ✅ ✍️ تا کمکتان کنیم.

**B3. Vague verb.** ✍️ A verb that only roughly says what happens.
❌ توضیحات محصول را از کاتالوگ سازنده می‌نویسد. ✅ ✍️ اطلاعات محصولات را از کاتالوگ سازنده استخراج می‌کند و در وب‌سایت شما اعمال می‌کند.
❌ عبارت‌های ترجمه‌ای را جمع می‌کند. ✅ ✍️ عبارت‌های ترجمه‌ای را جمع‌آوری می‌کند. (or «حذف می‌کند», depending on the meaning)
❌ قیمت را بالا و پایین می‌برد. ✅ ✍️ قیمت را بالا یا پایین می‌برد.

**B4. «به شما اجازه می‌دهد تا».** `[allows_you]`
❌ این ابزار به شما اجازه می‌دهد تا گزارش‌ها را دانلود کنید.
✅ ✍️ با این ابزار می‌توانید گزارش‌ها را دانلود کنید.

**B5. Pronoun spraying.** «شما … خود … خود» in one sentence. A possessive «شما» after a noun («مشتریان شما») is normal. `[pronoun_khod]`
❌ شما می‌توانید تنظیمات خود را در پنل کاربری خود تغییر دهید.
✅ ✍️ تنظیمات را از پنل کاربری تغییر دهید.

**B6. «اقدام به» and «انجام» nominalization.** «امکان X وجود دارد» is fine (D). `[nominal]`
❌ برای انجام ثبت‌نام، اقدام به وارد کردن شماره تلفن کنید.
✅ ✍️ برای ثبت‌نام، شماره تلفنتان را وارد کنید.

**B7. Cleft «این … است که».** ✍️ Calque of "It's you who …". `[cleft]`
❌ این شما هستید که تصمیم نهایی را می‌گیرید.
✅ ✍️ در نهایت، خودتان تصمیم نهایی را می‌گیرید.

**B8. Ezafe chain.**
❌ عبارت‌های ترجمه‌ای متن‌های هوش مصنوعی را جمع می‌کند.
✅ ✍️ عبارت‌های ترجمه‌ای را از متن‌های هوش مصنوعی جمع‌آوری می‌کند.

**B9. Em dash «—».** An appositive between two commas is fine. `[em_dash]`
❌ رصدبان — ابزار پایش قیمت رقبا — رایگان شد.
✅ ✍️ رصدبان، ابزار پایش قیمت رقبا، رایگان شد.

**B10. Adverb wedged between two commas.** ✍️ Used in Persian, but very rarely. `[parenthetical_adverb]`
❌ به سوال مشتری، حتی نصف‌شب، جواب می‌دهد.
✅ ✍️ حتی نصف‌شب هم جواب مشتری را می‌دهد.

**B11. Comma before «و» or «که».** ✍️ Never. A few exceptions may be added later. `[comma_before_va]`
❌ سفارش‌ها را همان روز بسته‌بندی می‌کنیم، و اگر تا ظهر ثبت شده باشند همان روز ارسال می‌شوند.

## C. Words and phrases

**C1. Intensifiers.** واقعاً، به‌سادگی، به‌راحتی، به‌طور یکپارچه، به‌طور کامل، بی‌نظیر. Drop most of them. `[intensifier]`
❌ به‌سادگی می‌توانید به‌طور یکپارچه با ابزارهای خود ادغام شوید.
✅ ✍️ به ابزارهایی که همین حالا با آن‌ها کار می‌کنید وصل می‌شود.

**C2. Translated collocations.** ✍️ Each row was confirmed by the copywriter, with their replacement. `[calque]`

| Translated | Source | Write instead ✍️ |
|---|---|---|
| تفاوت ایجاد کنید | make a difference | با آکسون، فروش فروشگاهتان را متفاوت کنید. |
| زمانتان را ذخیره کنید | save time | در زمان صرفه‌جویی کنید |
| به سطح بعدی ببرید | next level | ارتقا دهید |
| با ذهنی آسوده | peace of mind | با خیال راحت |
| مطمئن شوید که … | make sure | از صحت آدرس واردشده مطمئن شوید. / آدرس واردشده صحیح نیست. |
| هیجان‌زده‌ایم که … | we're excited to | مفتخریم که … |
| ۲۴/۷ | 24/7 | ۲۴ ساعته / شبانه‌روزی |
| یک کلیک و حسابتان فعال می‌شود | one click and … | حسابتان بلافاصله فعال می‌شود. (only when the reader might expect a wait) |
| لازم نیست … معذب شوید | no more awkward … | drop the feeling-word ✍️: «لازم نیست خودتان بارها پیگیری کنید.» |
| اگر باز هم مشکلی بود، ما هستیم. | we're here | fine in friendly and casual tone. In semi-formal and formal: اگر باز هم مشکلی داشتید، می‌توانید با ما در ارتباط باشید. |

**C3. Translated marketing imagery.** ✍️ «کرمای طلایی» is never used. This is about specific calqued images from English product copy, not about marketing language in general, which is welcome (section D).

**C4. Calqued boilerplate.** Usually replace these. ✍️ The rows marked "drop it" may be needed, depending on what the sentence means.

| Calque | Write instead |
|---|---|
| خوش برگشتید! | خوش آمدید |
| چیزی اشتباه پیش رفت | مشکلی پیش آمد |
| ما اینجا هستیم تا کمک کنیم | اگر مشکلی بود، به ما بگویید |
| موفقیت! (alone) | انجام شد / ذخیره شد |
| چیزی برای نمایش وجود ندارد | هنوز چیزی ثبت نشده |
| به جامعهٔ ما بپیوندید | عضو … شوید |
| در پایان روز | در نهایت |
| قدرت‌گرفته از X | بر پایهٔ X / با فناوری X |
| سفر شما با X | (usually drop it) |
| تجربهٔ کاربری بی‌نظیر | (usually drop it) |
| هرگونه سؤال | سؤالی |
| به نظر می‌رسد که | (usually drop it) |
| بدون هیچ‌گونه | بدون |
| ما معتقدیم که | (usually drop it) |

**C5. Coined word instead of an established loanword.** ✍️ «برنامهٔ وب»، «خوراک»، «پاورقی سایت»، «تصویر صفحه» where everyone says «وب‌اپلیکیشن»، «فید»، «فوتر»، «اسکرین‌شات». Don't turn «ایمیل» into «رایانامه». Lists in `terms.md` and `terms/`.

## D. Not tells: don't "fix" these

✍️ The copywriter rejected each of these as a rule. They are normal Persian. Don't rewrite a sentence because it contains one of them, and don't report them in editing mode.

- Passive with «توسط» («این گزارش توسط تیم پشتیبانی بررسی می‌شود»).
- «نه تنها … بلکه … نیز».
- Rhetorical questions and lead-ins («آیا تا به حال…؟»، «عجله دارید؟»).
- «در حال … هستید».
- Essay openings («در دنیای امروز …»).
- Colon + list («سه مزیت اصلی شامل: سرعت بالا، نصب آسان و پشتیبانی ۲۴ ساعته.»).
- Verbless fragments, in headlines and in product copy («سریع. امن. بدون دردسر.»، «اسپرسوساز مدل ES-20 خانگی.»).
- A comma between two related clauses («قیمت رقبا در ترب و باسلام هر روز تغییر می‌کنند، آکسون قیمت محصول‌هایتان را پابه‌پای آن‌ها بالا یا پایین می‌برد.» ✍️).
- «؛» used sparingly in formal and semi-formal tone.
- A three-part list of verb clauses, as long as each clause is complete and specific (B1 ✅).
- Sentence-initial «همچنین،»، «علاوه بر این،»، «این یعنی…»، «اینجاست که…»، «با استفاده از…».
- «معنی می‌دهد»، «X را تجربه کنید»، «در قلب X»، «راه‌حل‌ها»، «قدرتمند».
- A bureaucratic word beside a plain verb («جهت ثبت سفارش روی دکمه بزنید»).
- «امکان لغو سفارش وجود دارد».
- «سهم شما فقط مرور یک گزارش است» after a full lead-in (A3 ✅).
- «چرا باید X را انتخاب کنید؟» and «مشتریان دربارهٔ ما چه می‌گویند» as headings.
- Taglines such as «فروش آنلاین، بدون شب‌بیداری» or «سئو، بدون کارشناس سئو». (But «همیشه رقابتی، هرگز زیر کف» ✍️ reads as translated.)
- **Marketing.** ✍️ «پلاگین نباید جلوی موارد مارکتینگی را بگیرد.» Benefit framing («ایرفرایر AF-5 انتخابی هوشمندانه برای کسانی است که می‌خواهند …»), feeling and warmth, a short story on an about page, persuasive adjectives. The copywriter preferred these over a dry spec list in every blind pair where the skill had removed them.
- **Warm friendly email.** ✍️ «سلام دوست عزیز،»، «خبر خوب!»، «با مهر،», and one emoji in the subject line.
