## 2026-03-31 - Line Injection Prevention in JSON Lines Storage
**Vulnerability:** Unsanitized user input containing newline characters (`\n` or `\r`) injected into line-delimited JSON files (`registre_pionniers.json`).
**Learning:** Storing data as JSON Lines requires input validation against newline characters to prevent record injection or parser corruption when reading line-by-line.
**Prevention:** Validate input strings for newline characters (`\n`, `\r`) and strip whitespace before persisting to line-delimited log/database files.
