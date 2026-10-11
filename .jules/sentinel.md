## 2026-03-30 - Log Injection / CRLF Sanitization in Log Module
**Vulnerability:** `log_event.py` accepted raw input strings and appended them directly to `session_log.txt`. Malicious newline inputs (`\r`, `\n`) could forge fake timestamped log entries or obscure legitimate audit trails.
**Learning:** File-based logger functions that accept string inputs must sanitize line break characters (`\r`, `\n`) to prevent CRLF log injection / log forgery.
**Prevention:** Sanitize control characters and newlines in input strings before appending to flat file log streams, and validate string types.
