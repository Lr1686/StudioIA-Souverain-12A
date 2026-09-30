## 2026-03-30 - Newline Injection in Line-Delimited JSON Registers
**Vulnerability:** Unsanitized user input containing newline characters (`\n` or `\r`) injected into newline-delimited JSON data files (`JSONL`).
**Learning:** `inscrire_pionnier` wrote JSON entries directly followed by newlines and counted file lines to enforce registration caps. Unsanitized input with newlines could inject invalid JSON entries or corrupt line counts.
**Prevention:** Validate input type, strip leading/trailing whitespace, and reject inputs containing newline characters or excessive lengths before appending to JSONL files.
