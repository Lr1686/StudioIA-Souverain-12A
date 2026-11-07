## 2026-04-13 - CRLF Log Injection in Event Logging

**Vulnerability:** Unsanitized event strings written to `session_log.txt` in `log_event.py` allowed CRLF injection (`\r\n`), enabling attackers to forge sovereign log entries or tamper with audit trails.
**Learning:** Text-based log appending without stripping/replacing line break characters treats newlines as record delimiters, allowing malicious actors to simulate valid timestamped entries.
**Prevention:** Sanitize log entries by replacing `\r` and `\n` with spaces, validating input types and rejecting empty or oversized messages before writing.
