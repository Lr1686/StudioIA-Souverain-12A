## 2026-04-13 - Log Injection Vulnerability in Event Recorder
**Vulnerability:** Unsanitized user/event input logged directly to text files allowed log injection via newline sequences (`\n`, `\r`), enabling attackers to forge log entries or corrupt log formatting.
**Learning:** File logging without newline escaping allows malicious inputs to split single events into fake multi-line entries, bypassing log audit integrity.
**Prevention:** Always escape or strip newline characters (`\n` and `\r`) from inputs prior to string formatting and file output in plain-text logging tools.
