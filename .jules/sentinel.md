## 2026-04-13 - Prevent Log Injection (CWE-117) in event logging
**Vulnerability:** Unsanitized user inputs written directly into event log files allowed log injection/forging via embedded newline characters (`\n`, `\r`) and control codes.
**Learning:** Hardcoded path constants in functions prevent isolated test mocking with `monkeypatch.setattr`, causing test runs to inadvertently dirty production/application log files.
**Prevention:** Always expose target paths as module-level configurable constants (`LOG_PATH = ...`) and sanitize all inputs before formatting into structured text log entries.
