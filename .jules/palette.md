## 2026-03-29 - CLI Input Validation & Clear Feedback
**Learning:** CLI utilities receiving interactive or programmatically passed user strings should immediately validate empty/whitespace input before running side-effects or allocating state, returning actionable warning messages.
**Action:** Always trim input strings and guard against empty inputs early in CLI helper functions.
