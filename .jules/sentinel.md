## 2026-03-31 - Log Injection Prevention in Event Logging
**Vulnerability:** Unsanitized event messages containing control characters or newline sequence (`\n`, `\r`) permitted log injection and formatting corruption in `session_log.txt`.
**Learning:** Writing raw string inputs to file logs without filtering allowed multiline fake log injection.
**Prevention:** Always validate type and maximum length, strip leading/trailing whitespace, and sanitize control characters (`ord(c) < 32 or ord(c) == 127`) prior to logging.
