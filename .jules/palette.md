## 2026-03-30 - Text-based capacity progress indicator in CLI workflows

**Learning:** Terminal-based user interfaces often display quota information purely as raw numerical values. Providing a dual representation with both numerical remaining/total capacity and a visual text progress meter (e.g. `[■■■□□□□□□□]`) improves comprehension at a glance for screen reader users and visual CLI users alike.
**Action:** When displaying limited capacity or finite slots in CLI applications, combine fraction counts with accessible unicode progress blocks (`■`/`□`).
