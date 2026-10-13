## 2026-03-30 - Input Validation and Log Injection Prevention Pattern
**Vulnerability:** Unsanitized user inputs written to flat file logs or JSON databases could allow log forgery, CRLF injection, or unhandled errors.
**Learning:** Functions accepting text strings for filesystem logging or registry storage should validate type, length, and disallow control characters (`ord(c) < 32 or ord(c) == 127`).
**Prevention:** Apply input validation checking `isinstance(s, str)`, length constraints, non-emptiness, control character checks, and guard file path directory creation before writing files.
