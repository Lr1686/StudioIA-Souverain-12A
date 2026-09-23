## 2026-03-29 - Path Validation and Strict Directory Scope Enforcment
**Vulnerability:** Unrestricted path usage in JSON storage operations allowed potential path traversal or unexpected file write locations if `DB_PATH` is overridden or improperly concatenated.
**Learning:** Checking path containment with `os.path.abspath` against `DATA_DIR + os.sep` ensures path containment while avoiding false positives with similar prefix folder names.
**Prevention:** Always validate resolved file paths using `_get_safe_path` before reading or writing files.
# Sentinel Journal

Security learnings and notes for this repository.
