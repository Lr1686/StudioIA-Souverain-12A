## 2026-04-13 - Log Injection (CWE-117) via Unsanitized Event Messages

**Vulnerability:** In `log_event.py`, user-supplied or external `message` arguments were directly concatenated into single-line structured session logs (`session_log.txt`) without newline, carriage return, control character, or length validation. An attacker could inject CRLF characters to forge arbitrary audit trail entries (log injection / forging) or corrupt log parsers.
**Learning:** Logging utilities writing to plain-text structured audit logs require strict input sanitization preventing control characters (especially `\r` and `\n`) and enforcing length boundaries, in alignment with defense-in-depth sanitization applied across other system ingress points (like `gestion_pionniers.py`).
**Prevention:** Always validate that incoming event log strings are strictly non-empty strings, contain no control characters (< 32, 127), and adhere to reasonable upper size limits before writing to persistent logs.
