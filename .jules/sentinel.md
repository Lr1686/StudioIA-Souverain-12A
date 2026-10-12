## 2026-03-30 - Log Injection (CWE-117) Prevention in Event Logging

**Vulnerability:** Unsanitized user inputs passed to `enregistrer_evenement` in `log_event.py` allowed log forgery / log injection (CWE-117) via newline (`\n`, `\r`) characters, enabling fake log entries to be written into session log files.
**Learning:** Raw string concatenation into log files without line break sanitization permits attackers to inject fraudulent timestamps and arbitrary log messages, undermining log integrity.
**Prevention:** Always validate input type and replace carriage returns (`\r`) and newlines (`\n`) with spaces or strip control characters before formatting log entries.
