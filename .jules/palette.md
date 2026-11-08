## 2026-03-30 - Text-based capacity progress indicator in CLI workflows

**Learning:** Terminal-based user interfaces often display quota information purely as raw numerical values. Providing a dual representation with both numerical remaining/total capacity and a visual text progress meter (e.g. `[■■■□□□□□□□]`) improves comprehension at a glance for screen reader users and visual CLI users alike.
**Action:** When displaying limited capacity or finite slots in CLI applications, combine fraction counts with accessible unicode progress blocks (`■`/`□`).

## 2026-03-30 - Actionable terminal errors for missing configuration files

**Learning:** CLI utilities reporting missing prerequisite files often print generic failure notices without context. Specifying the exact expected file path along with concrete next steps helps users diagnose environment misconfigurations immediately.
**Action:** In CLI initialization scripts, include the target file path and an explicit verification directive in error messages rather than a generic failure string.
