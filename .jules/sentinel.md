## 2026-04-13 - Prevent Log Injection (CWE-117) in Event Logging
**Vulnerability:** Unsanitized user inputs passed to `enregistrer_evenement` allowed newlines and control characters in log entries, enabling log forging and structure corruption.
**Learning:** Python file writes appending unescaped strings to text log files are vulnerable to log injection if inputs contain `\r` or `\n`.
**Prevention:** Filter control characters (`ord(c) < 32 or ord(c) == 127`) in logging helper functions before appending messages to log files.
