## 2026-03-30 - Prevent CRLF Log Injection (CWE-117) in file logging

**Vulnerability:** Unsanitized user/system message parameters in `log_event.py` allowed inserting carriage returns (`\r`) and newlines (`\n`), enabling log forging / fake entry injection.
**Learning:** Writing raw string variables to line-oriented log files (`.txt` / `.log`) without replacing newline characters permits malicious actors to craft entries with arbitrary timestamps and fake severities.
**Prevention:** Sanitize input strings by converting `\r` to `\r` and `\n` to `\n` before formatting into log entries, and validate string types.
