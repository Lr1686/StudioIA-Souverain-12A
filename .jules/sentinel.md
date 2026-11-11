## 2026-04-13 - Log Injection (CWE-117) and Input Validation in Event Logging

**Vulnerability:** `enregistrer_evenement` in `log_event.py` appended untrusted input strings directly to `DATA/LOGS_SOUVERAINS/session_log.txt` without checking for CRLF characters (`\r`, `\n`) or limiting message length. An attacker could forge false audit log lines, tamper with security tracking, or cause disk exhaustion.
**Learning:** File append logging routines in minimalist CLI tools frequently miss CRLF sanitization, enabling log spoofing and record injection when arbitrary user input is accepted.
**Prevention:** Explicitly validate message type, enforce maximum character limits, and reject any control or newline characters (`ord(c) < 32 or ord(c) == 127`) before formatting log entries.
