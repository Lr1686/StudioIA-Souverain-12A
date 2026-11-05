## 2026-04-13 - Log Injection (CWE-117) and Input Validation in Audit Trails

**Vulnerability:** `enregistrer_evenement` in `log_event.py` accepted unvalidated strings and directly appended them to `session_log.txt`. Attackers or untrusted input could inject newlines (`\n`, `\r`) to spoof session log records or supply excessively large inputs leading to log file bloat / DoS.
**Learning:** File-based text logging in CLI applications must explicitly sanitize control characters (< 32, 127) and enforce max string length limits to preserve audit log integrity and prevent log forging.
**Prevention:** Always validate input type, enforce character boundaries (`any(ord(c) < 32 or ord(c) == 127)`), enforce length caps, and strip untrusted inputs before appending to flat-file logs.
