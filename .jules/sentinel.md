# Sentinel Security Journal

## 2026-03-31 - JSON Lines Injection & Unvalidated Input
**Vulnerability:** `inscrire_pionnier` accepted unsanitized string input written directly as JSON lines into `registre_pionniers.json`. Unescaped newline characters could corrupt the JSON line structure or inject fake entries.
**Learning:** File-based text storage (such as `.jsonl` / line-delimited JSON) requires input validation to strip/reject newline characters and control character injection, along with length limits to avoid DoS/storage exhaustion.
**Prevention:** Validate input type, string length, and sanitize/reject newline characters (`\r`, `\n`) before appending records to JSON line files.
