---
type: regex
target: { source: file, path: "src/Auth.tsx" }
pattern: '[يك]|(?<![\u0600-\u06FF\u200c])ن?می (?=[\u0600-\u06FF])'
match: not_contains
---
