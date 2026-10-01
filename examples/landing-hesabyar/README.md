# نمونه: صفحهٔ اول «حساب‌یار»، بدون هم‌قلم و با هم‌قلم

هر چهار فایل این پوشه خروجی واقعی Claude Code است و دستی ویرایش نشده‌اند. تاریخ تولید ۲۰۲۶-۱۰-۰۱ است و نسخهٔ هم‌قلم ۴٫۰٫۰. این بریف ربطی به نمونه‌های کپی‌رایتر در `skills/hamghalam/references/genres/` ندارد، پس خروجی از آن نمونه‌ها کپی نشده است. این خروجی‌ها را کپی‌رایتر هنوز داوری نکرده است.

| فایل | چه چیزی است |
|---|---|
| `1-without-skill.md` | صفحهٔ کامل، نوشتهٔ Claude Code بدون هیچ پلاگین یا اسکیل فارسی |
| `2-with-skill.md` | همان متن، ویرایش‌شده با هم‌قلم در حالت ویرایش |
| `2-with-skill-report.md` | گزارش سه‌سطحی‌ای که هم‌قلم کنار ویرایش نوشت (✅ اعمال‌شده، ⚠️ پیشنهاد، ⏭ خارج از دامنه) |
| `3-with-skill-warnings-approved.md` | همان ویرایش، بعد از آن‌که کاربر پیشنهادهای ⚠️ را تأیید کرد |

## چرا نسخهٔ ۲ کم تغییر کرده است

در حالت ویرایش، هم‌قلم عمداً محتاط است:
- **فقط نشانه‌های تأییدشده را عوض می‌کند.** این‌ها نشانه‌هایی‌اند که کپی‌رایتر تأیید کرده است، یعنی دکمه‌ها و تیترهای ستون «نه» در `frames.md`، زبان گفتاری و جملهٔ شعاری.
- **تیترها پیش‌فرض ⚠️ می‌مانند.** تیتر و شعار متن تبلیغاتی‌اند، پس هم‌قلم آن‌ها را بدون تأیید کاربر عوض نمی‌کند.
- **به ساختارهای بخش D دست نمی‌زند.** این‌ها ساختارهایی‌اند که کپی‌رایتر طبیعی دانسته، مثل ویرگول بین دو جملهٔ مرتبط.

نسخهٔ ۳ نشان می‌دهد وقتی کاربر پیشنهادها را تأیید می‌کند چه اتفاقی می‌افتد.

## بریف و دستورها

متن بدون اسکیل را این دستور ساخت. بریف عمداً انگلیسی است، چون برنامه‌نویس‌ها معمولاً همین‌طور می‌نویسند:

```
claude -p "We're launching the Persian website for Hesabyar (حساب‌یار), an online invoicing and accounting app
for small Iranian businesses. Facts: it issues official sales invoices and sends them to the Moadian tax system
(سامانهٔ مؤدیان) automatically; it tracks who still owes you money and sends payment reminders by SMS; it has
Android and iOS apps; data is backed up daily on servers inside Iran; there is a 14-day free trial, no credit
card needed; plans start at 290,000 tomans per month.
Write the complete Persian landing page in semi-formal tone: hero (headline, subheadline, main button), a features
section, a 'How it works' section, a pricing teaser, a short FAQ with 3 questions, and a closing call to action.
Save it as landing.md."
```

ویرایش با هم‌قلم:

```
claude -p --plugin-dir path/to/HamGhalam "با هم‌قلم این متن صفحهٔ اول سایت (فایل landing.md) را ویرایش کن.
لحن نیمه‌رسمی است و همهٔ متن در دامنه است. نسخهٔ نهایی را در فایل landing.hamghalam.md بنویس و گزارش کامل
ویرایش (سه‌سطحی) را در فایل report.md بنویس. خود landing.md را تغییر نده."
```

تأیید پیشنهادها:

```
claude -p --plugin-dir path/to/HamGhalam "با هم‌قلم: گزارش ویرایش report.md را خواندم. همهٔ پیشنهادهای بخش ⚠️
را تأیید می‌کنم، به‌جز مورد «ثبت‌نام کنید» که بماند. آن‌ها را روی landing.hamghalam.md اعمال کن و نتیجه را در
landing.hamghalam.approved.md بنویس."
```

## مهم‌ترین تفاوت‌ها

| بدون هم‌قلم | با هم‌قلم | قاعده |
|---|---|---|
| دکمه: «۱۴ روز رایگان امتحان کنید» و «همین حالا رایگان شروع کنید» | «ثبت‌نام رایگان» | `frames.md` |
| تیتر: «چطور کار می‌کند؟» | «مراحل راه‌اندازی» | `frames.md` |
| تیتر: «هر آنچه کسب‌وکار کوچک شما لازم دارد» | «امکانات حساب‌یار» (نسخهٔ ۳) | `frames.md` |
| «کسب‌وکارتان همیشه همراه شماست. از موبایل فاکتور صادر کنید و وضعیت حساب‌ها را هر جا که هستید ببینید.» | «با اپلیکیشن حساب‌یار روی موبایل هم می‌توانید فاکتور صادر کنید و وضعیت بدهی‌ها و طلب‌هایتان را ببینید.» | `patterns.md` B2 (اسم ناگفته) |
| «پیامک یادآوری می‌رود» | «پیامک یادآوری برایش ارسال می‌شود» | `patterns.md` A1 (زبان گفتاری) |
| «اگر خوشتان نیامد، هیچ تعهدی ندارید.» | «اگر راضی نبودید، تعهدی برای ادامه ندارید.» (نسخهٔ ۳) | `patterns.md` A1 |
