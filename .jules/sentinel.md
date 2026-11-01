## 2026-03-30 - CWE-117 Log Injection in Event Logging

**Vulnerability:** `enregistrer_evenement` in `log_event.py` appended user/caller provided string messages directly to text log files without validating input type or sanitizing newline (`\r`, `\n`) and unprintable control characters. Attackers or corrupted inputs could forge fake log lines or alter log parsing structure.
**Learning:** Even internal helper scripts writing to session logs must sanitize message inputs by replacing/stripping newlines and control characters, validating string type, and ensuring the parent logging directory exists safely.
**Prevention:** Always validate string input types and sanitize against control characters (especially CRLF) before writing to flat-file log streams.
