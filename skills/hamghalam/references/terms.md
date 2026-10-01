# Term glossary — core

This file is short and is **always read**. It holds only the one rule that applies to every domain: which English loanwords are already naturalized in Persian and which aren't. Domain-specific word lists (tech, finance, retail, …) live in `references/terms/` and are loaded **only when the domain is known** — see "Domain-specific lists" below.

Each row reports a common convention, not a law. If a word means something else in your sentence, reject it.

## General loanword rule

Don't Persianize established loanwords; do translate words that haven't caught on.

| Established — write it as is | Not established — translate it |
|---|---|
| ایمیل، لینک، اپلیکیشن، اپ، دانلود، آپدیت، پروفایل، داشبورد، پنل، تیکت، پلن، فیلتر، دامنه، هاست، لاگ، کش، بک‌آپ، فید، فوتر، هدر، استیکر، منشن، اسکرین‌شات، اکانت، تم، پلاگین، ویجت، API، URL | feature → قابلیت · seamless → (drop it) · leverage → استفاده از · insight → دید / تحلیل · empower → (drop it) · robust → پایدار · streamline → ساده‌کردن · onboarding → شروع کار / راه‌اندازی · engagement → تعامل · journey → (drop it) |

## Domain-specific lists

Tell C5 in `patterns.md` (coined word instead of an established loanword) needs a domain lookup to catch the long tail. Don't load all of them by default — that reintroduces the exact context bloat v2 of this skill removed (see `CHANGELOG.md`, v2.0.0). Instead:

1. Figure out the domain from the user's request or the project's existing content (e-commerce store, crypto exchange, SaaS dashboard, …) — this is the same judgment call step 0 already makes for tone, not a separate classifier.
2. Read the matching file(s) under `references/terms/` (currently `tech.md`, `finance.md`, `retail.md`).
3. If the domain is ambiguous or the text spans more than one (e.g. a fintech app touches both `tech.md` and `finance.md`), read all plausible candidates — each file is small, so reading two or three costs far less than the old single giant glossary ever did.
4. If nothing fits, skip this step; the general rule above plus `patterns.md` still cover most of the real violations.

None of this limits `scripts/lint.py`: the linter always reads every file under `references/terms/` plus this core file from disk, at zero token cost, regardless of which ones you loaded into context. So even a wrong or skipped domain guess during writing gets caught by the automatic lint pass after the file is saved (see `hooks/post_write_lint.py` at the plugin root).
