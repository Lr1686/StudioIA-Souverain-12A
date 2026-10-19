## 2026-03-30 - CWE-117 Log Injection Prevention in Custom Text Loggers

**Vulnerability:** Unsanitized user inputs passed to text loggers in `log_event.py` permitted Log Injection / Log Forgery (CWE-117) via newline characters (`\n`, `\r`) and ASCII control characters, allowing line splitting and fake log entry injection.
**Learning:** For custom text-based logging where events are appended line-by-line, any newline characters in message payloads break log file structure and log parsing integrity.
**Prevention:** Always sanitize log messages by replacing `\n` and `\r` with escaped representations (`\n`, `\r`) and stripping/escaping control characters (`ord(c) < 32`), ensuring each log event strictly occupies a single line.
