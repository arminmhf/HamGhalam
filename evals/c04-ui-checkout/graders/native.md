---
type: llm
focus: { source: file, path: "src/Checkout.tsx" }
---

You are judging Persian (Farsi) website copy. Judge only the Persian text in the file.

PASS only if ALL of these hold:
- Sentences are connected and descriptive the way Persian prose is written; the text is NOT a run of short, clipped sentences or verbless fragments in body text (headlines may be short).
- No section heading is a literal translation of an English landing-page frame such as «چه کاری برایتان انجام می‌دهد», «چرا باید X را انتخاب کنید؟», «آماده‌اید شروع کنید؟».
- The text does not end a section with an English-style punchline addressed to the reader (e.g. «شما فقط گزارش را می‌بینید», «سهم شما فقط …»).
- No English-calque idioms (e.g. «بیایید…», «به سطح بعدی»، «این فقط یک X نیست»، «یک کلیک و …»، «ما هستیم»).

FAIL if any of these is violated. When unsure, FAIL.
