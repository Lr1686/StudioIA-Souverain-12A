## 2025-05-10 - Log Injection Neutralization (CWE-117)
**Vulnerability:** Unsanitized user input passed to `log_event.enregistrer_evenement` allowed log forgery/CRLF injection into system session logs (`session_log.txt`).
**Learning:** File logging utilities must sanitize newline (`\n`, `\r`) and control characters from event messages before formatting entry strings.
**Prevention:** Neutralize carriage returns and newlines with space replacements and validate that input is a non-empty string prior to log file output.
