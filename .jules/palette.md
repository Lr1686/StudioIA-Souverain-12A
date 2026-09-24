## 2026-03-30 - Interactive CLI validation and feedback

**Learning:** Interactive CLI scripts that prompt for user input (such as `inscrire_pionnier`) can accept empty or whitespace-only inputs without proper sanitization and validation, leading to blank database entries. Adding string whitespace trimming (`nom.strip()`) and explicit validation feedback ensures data integrity and a clear, helpful user experience.
**Action:** Always validate and sanitize user input strings from CLI prompts and output actionable error messages before performing state modifications.
