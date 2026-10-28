## 2026-04-13 - Neutralize CRLF and Control Characters in Plain-Text Logging
**Vulnerability:** Unsanitized event messages passed to `log_event.py` allowed log injection (CRLF injection), enabling malicious inputs containing `\n` to forge timestamped log entries in `session_log.txt`.
**Learning:** Plain-text loggers appending formatted strings are vulnerable to line forgery if raw user or event strings contain line breaks or ASCII control characters.
**Prevention:** Sanitize all string inputs logged to line-delimited files by replacing `\n`, `\r`, and control characters (`ord(c) < 32 or ord(c) == 127`) before formatting log entries.
