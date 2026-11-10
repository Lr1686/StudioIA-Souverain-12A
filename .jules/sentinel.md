## 2026-04-13 - Log injection (CWE-117) and unbounded writes in plain-text audit logs

**Vulnerability:** In `log_event.py`, `enregistrer_evenement` directly appended arbitrary caller-supplied strings into `session_log.txt`. Unvalidated input allowed newline characters (`\n`, `\r`) enabling log forging of fake sovereign events and timestamps, as well as unconstrained message lengths posing a denial-of-service risk.
**Learning:** File-based linear text audit logs rely strictly on single-line entry contracts. Any raw multi-line strings break the integrity of the audit trail and can mislead incident response or integrity verification scripts.
**Prevention:** Strictly validate string type, enforce a maximum length cap, and strip or reject non-printable/control characters (`ord(c) < 32` or `127`) before writing to file-based logs.
