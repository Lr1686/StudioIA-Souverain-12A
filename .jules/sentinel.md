## 2026-11-06 - Log Injection (CWE-117) and Input Validation in Audit Logs

**Vulnerability:** In `log_event.py`, `enregistrer_evenement` appended arbitrary message strings into the single-line formatted sovereignty audit log (`DATA/LOGS_SOUVERAINS/session_log.txt`) without validation or sanitization. Attackers or untrusted callers could supply newline (`\n` or `\r`) sequences to forge arbitrary log records, spoof timestamps, fabricate system events, or exhaust disk space via oversized payloads.
**Learning:** File-based flat audit logging functions that format entries with timestamps assuming single-line records are susceptible to log injection (log forging) if raw user or external inputs are accepted without verifying the absence of control/newline characters and length limits.
**Prevention:** Strictly enforce type checks, maximum length limits, non-empty content validation, and reject control characters (`ord(c) < 32 or ord(c) == 127`) before formatting log entries.
