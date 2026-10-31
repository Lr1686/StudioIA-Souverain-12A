## 2026-10-31 - Log Injection prevention via control character sanitization

**Vulnerability:** `log_event.py` accepted raw input strings and wrote them unescaped to `session_log.txt`. Attackers could inject newline characters (`\n` or `\r`) to spoof arbitrary log timestamps or manipulate sovereign audit trail logs (CWE-117).
**Learning:** File-based newline-delimited logs are vulnerable to log forging unless control characters (ASCII < 32 and DEL 127) and length boundaries are strictly validated before write.
**Prevention:** Always validate string types, strip whitespace, enforce max length, reject non-printable/control characters, and ensure target directories exist before persisting log entries.
