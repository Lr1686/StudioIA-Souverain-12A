## 2026-03-30 - Log Injection (CWE-117) prevention in text logging

**Vulnerability:** Unsanitized user inputs written directly to flat log files allowed potential log forgery / injection attacks via embedded newline characters (`\n`, `\r`) or control characters.
**Learning:** Functions that accept string messages for file logging must enforce type checking, prohibit control characters and unescaped newlines, and ensure log target parent directories exist (`os.makedirs(..., exist_ok=True)`).
**Prevention:** Always validate and sanitize log entry inputs against non-printable ASCII and newline injection prior to formatting or writing to log storage.
