## 2026-03-01 - Prevent Log Injection (CWE-117) in Event Logger
**Vulnerability:** `enregistrer_evenement` in `log_event.py` appended unescaped user messages to `session_log.txt`. An attacker could inject `\n` or `\r` characters into `message` to forge fake log entries (e.g., false status messages or severity levels).
**Learning:** File-based event logging functions accepting external messages must strip/replace line breaks before formatting into single-line log structures.
**Prevention:** Sanitize `\r` and `\n` characters from string parameters prior to formatting and writing log entries.
