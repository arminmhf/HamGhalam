---
type: llm
focus: { source: file, path: "out.md" }
---

The input text was written by a Persian copywriter. Its only real problems were mechanical: missing half-spaces (ZWNJ) such as «میکند», «قیمت های», «وبسایت», «کار های». The second sentence uses «توسط» and «نه تنها … بلکه … نیز», which the copywriter considers normal Persian.

PASS if the edited text in the file keeps the copywriter's wording and sentence structure essentially unchanged (fixing spacing, ZWNJ and spelling is expected; a light touch on the second sentence is acceptable), and keeps the long first sentence as one sentence.
FAIL if it rewrites the text substantially, splits the first sentence into several short sentences, makes the register more colloquial, or rewrites the «توسط» / «نه تنها … بلکه» sentence only because of those constructions.
