## 2026-03-30 - Log Injection & Control Character Filtering

**Vulnerability:** Unsanitized user inputs in `log_event.py` allowed forged log entries via newline injection (`\n`, `\r`) and unbounded log file growth (DoS risk).
**Learning:** `ord(c) < 32 or ord(c) == 127` effectively filters ASCII control characters and newline injections while preserving multi-byte non-ASCII characters (e.g. accented UTF-8 letters above 127).
**Prevention:** Always validate input type, string length, and check for ASCII control characters (`\n`, `\r`, `\t`, `\x00`) before appending raw user strings to structured text log files.
