---
type: regex
target: { source: file, path: "out.md" }
pattern: '[يك]|(?<![؀-ۿ‌])ن?می (?=[؀-ۿ])|میکند|میدهد'
match: not_contains
---
