## 2026-04-13 - Log Injection (CWE-117) and Denial-of-Service via Unsanitized Logging

**Vulnerability:** `log_event.enregistrer_evenement` wrote arbitrary, unvalidated strings directly into the sovereign log file `DATA/LOGS_SOUVERAINS/session_log.txt`. Attackers could inject newline characters (`\n`, `\r`) to forge sovereign timestamped audit entries or supply unbounded payloads causing storage exhaustion.
**Learning:** Shared event logging and telemetry functions are frequently invoked with external parameters. Without strict input validation, length bounding, and control-character filtering, log forgery breaks the audit integrity of the system.
**Prevention:** Always validate data type, enforce maximum string length, reject or sanitize unescaped control characters (ASCII < 32 and 127), and ensure destination directories exist defensively before writing log files.
