## 2026-03-30 - CLI Input Validation & User Feedback

**Learning:** CLI scripts accepting interactive user input (e.g. `gestion_pionniers.py`) can fail silently or register invalid entries when empty or whitespace-only inputs are passed without validation.
**Action:** Always sanitize inputs with `.strip()` and provide clear, actionable feedback messages with standard status indicators (e.g., `⚠️ NOM INVALIDE`) before persisting records.
