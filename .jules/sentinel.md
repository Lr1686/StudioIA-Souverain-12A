## 2026-04-13 - Line-Delimited JSON Input Injection and DoS Protection
**Vulnerability:** Unsanitized user inputs containing newlines or excessive length in line-delimited JSON data stores can corrupt log files or cause storage DoS.
**Learning:** Checking for printable characters and enforcing maximum input lengths prevents format breaking and unbounded storage growth in simple JSON/log files.
**Prevention:** Always validate data type, filter out non-printable/newline control characters, and enforce character length limits on user-supplied parameters before writing to flat files or line-delimited JSON files.
