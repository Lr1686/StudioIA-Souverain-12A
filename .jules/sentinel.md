## 2026-04-13 - Log Injection (CWE-117) Sanitization and Length Enforcing

**Vulnerability:** Unsanitized user/event messages written directly to session logs allowed forging log entries via newline (`\n`, `\r`) injection and potential unbounded log file bloating.
**Learning:** File append logging routines in CLI utilities without a framework logger must explicitly strip/sanitize control characters (`ord(c) < 32` or `127`) and enforce length limits before appending.
**Prevention:** Sanitize newlines and control characters, limit message length to 500 characters, and ensure parent directories exist prior to file I/O operations.
