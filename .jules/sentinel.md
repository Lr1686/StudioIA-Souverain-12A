## 2026-03-30 - Log Injection (CWE-117) via un-sanitized log messages

**Vulnerability:** Messages logged to `DATA/LOGS_SOUVERAINS/session_log.txt` via `log_event.py` were written directly without sanitizing newline characters (`\n`, `\r`), allowing attackers to forge arbitrary log lines or manipulate log records.
**Learning:** Functions accepting external strings for event logging must strip or escape newline characters to prevent multiline log forgery.
**Prevention:** Replace carriage returns (`\r`) and line breaks (`\n`) with escaped character sequences (`\\r` and `\\n`) prior to formatting and writing log entries.
