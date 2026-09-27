## 2026-03-30 - Inline validation feedback for CLI user input

**Learning:** Interactive CLI scripts that accept user input without empty/whitespace input validation lead to bad user experience and invalid data entries. Returning clear error messages (`❌ ERREUR : ...`) early prevents corrupted entries and improves interaction clarity.
**Action:** Always validate and strip string user inputs in CLI tools before processing or writing to storage.
