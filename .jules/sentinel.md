## 2026-04-13 - Log Injection (CRLF) Prevention in Flat-File Sovereign Audit Logs

**Vulnerability:** Flat-file event logging (`DATA/LOGS_SOUVERAINS/session_log.txt`) via `enregistrer_evenement()` concatenated unvalidated input into single-line log records, allowing CRLF injection / log forging (CWE-117) and uncontrolled log expansion.
**Learning:** In projects using plain text append-only audit files, every logging entry function is an input sink. Without strict validation rejecting newlines (`\r`, `\n`), ASCII control characters (`< 32` or `127`), and length caps, attackers can fabricate trusted log lines or corrupt log format.
**Prevention:** Always validate that logged messages are strings, reject control characters / CRLF sequences, enforce length boundaries, and ensure destination directory creation is guarded before appending.
