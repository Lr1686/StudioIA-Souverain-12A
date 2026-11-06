## 2026-03-30 - Text-based capacity progress indicator in CLI workflows

**Learning:** Terminal-based user interfaces often display quota information purely as raw numerical values. Providing a dual representation with both numerical remaining/total capacity and a visual text progress meter (e.g. `[■■■□□□□□□□]`) improves comprehension at a glance for screen reader users and visual CLI users alike.
**Action:** When displaying limited capacity or finite slots in CLI applications, combine fraction counts with accessible unicode progress blocks (`■`/`□`).

## 2026-03-30 - Actionable recovery guidance for missing configuration errors in CLI interfaces

**Learning:** Generic terminal error messages (e.g. "ERREUR : Le noyau d'identité est manquant.") leave CLI users confused about the root cause and next steps. Providing clear visual signposts (`⚠️ ERREUR :`, `✅`, `💡 CONSEIL :`) along with the exact file path that was attempted and an actionable suggestion enables users and terminal readers to immediately understand and remediate system state issues.
**Action:** In CLI scripts that depend on local file assets, always show the exact missing path and an actionable hint alongside standardized status icons.
