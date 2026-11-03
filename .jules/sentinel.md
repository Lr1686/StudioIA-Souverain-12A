# Sentinel Security Journal

## 2026-03-31 - JSON Lines Injection & Unvalidated Input
**Vulnerability:** `inscrire_pionnier` accepted unsanitized string input written directly as JSON lines into `registre_pionniers.json`. Unescaped newline characters could corrupt the JSON line structure or inject fake entries.
**Learning:** File-based text storage (such as `.jsonl` / line-delimited JSON) requires input validation to strip/reject newline characters and control character injection, along with length limits to avoid DoS/storage exhaustion.
**Prevention:** Validate input type, string length, and sanitize/reject newline characters (`\r`, `\n`) before appending records to JSON line files.

## 2026-04-14 - Log Injection / Log Forgery (CWE-117)
**Vulnerability:** `enregistrer_evenement` in `log_event.py` appended unvalidated messages directly to `session_log.txt`. Unescaped newline (`\n`) and carriage return (`\r`) characters allowed forging fake log entries or spoofing system events.
**Learning:** Raw string interpolation into plain text event logs without character filtering allows adversaries to inject arbitrary log lines, falsifying audit trails and obfuscating malicious activity.
**Prevention:** Sanitize line break characters (`\r`, `\n`) by stripping or replacing them with spaces, validate input types, and ensure parent directory exists before appending log entries.
