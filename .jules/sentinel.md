## 2026-03-30 - CWE-117 Log Injection in Sovereignty Event Logging

**Vulnerability:** In `log_event.py`, raw event messages were formatted and appended directly to `DATA/LOGS_SOUVERAINS/session_log.txt` without sanitizing newlines (`\r`, `\n`) or control characters, allowing attackers or untrusted inputs to forge log entries or tamper with audit records.
**Learning:** File-based flat-text append loggers are susceptible to log injection when messages are not validated and stripped of newline characters before emission.
**Prevention:** Always validate that incoming log messages are valid strings, and sanitize all control characters and line terminators (replacing with spaces) before appending to log files.
