## 2026-04-13 - Log Injection (CWE-117) and Input Validation in File Logging

**Vulnerability:** `log_event.py` appended unvalidated and unsanitized message strings directly to flat session log files (`DATA/LOGS_SOUVERAINS/session_log.txt`), allowing attackers or external callers to forge log entries via newline (`\n`, `\r`) injection and cause unbounded file growth.
**Learning:** Even internal CLI logging utilities that write to flat text logs require explicit control character and newline rejection (`ord(c) < 32 or ord(c) == 127`) and length caps to preserve audit integrity and prevent denial of service.
**Prevention:** Always validate data type, enforce maximum payload size, reject/sanitize control characters and newline delimiters prior to appending into plain-text audit logs.
