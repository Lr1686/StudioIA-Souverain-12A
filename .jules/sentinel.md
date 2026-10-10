## 2026-03-30 - Log Injection (CWE-117) Mitigation in Event Logging

**Vulnerability:** Untrusted log message inputs in `log_event.py` could contain embedded newlines (`\r`, `\n`) or control characters, enabling log injection / log forging attacks that fabricate fake log entries or mangle log streams.
**Learning:** Accepting raw string input for plain-text file logging without stripping newlines and control characters allows malicious inputs to inject arbitrary timestamped log entries into persistent log files.
**Prevention:** Always validate that log inputs are strings, replace carriage returns and newlines with spaces, strip control characters (`ord(c) < 32 or ord(c) == 127`), and ensure log output paths exist before file I/O operations.
