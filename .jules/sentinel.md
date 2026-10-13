## 2026-03-30 - Log Injection & Missing Directory Defense in `log_event.py`
**Vulnerability:** Unsanitized user messages logged to text files permitted Log Injection (CRLF/newline injection) and could fail if parent directories did not exist.
**Learning:** Event logging functions accepting string messages must strip control characters (`ord(c) < 32` or `127`) to prevent attackers from inserting fake timestamps/log entries.
**Prevention:** Always sanitize control characters/newlines and verify parent directory existence before opening log files in append mode.
