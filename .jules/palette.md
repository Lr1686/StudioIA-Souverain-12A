## 2026-03-30 - Text-based capacity progress indicator in CLI workflows

**Learning:** Terminal-based user interfaces often display quota information purely as raw numerical values. Providing a dual representation with both numerical remaining/total capacity and a visual text progress meter (e.g. `[■■■□□□□□□□]`) improves comprehension at a glance for screen reader users and visual CLI users alike.
**Action:** When displaying limited capacity or finite slots in CLI applications, combine fraction counts with accessible unicode progress blocks (`■`/`□`).

## 2026-03-30 - Actionable Hierarchical Diagnostics in CLI System Checks

**Learning:** In terminal health check scripts, displaying an aggregate warning state (such as "DÉSYNCHRONISATION DÉTECTÉE") without identifying the specific failing checks forces users into guesswork. Using an indented hierarchical sub-bullet pattern (e.g. `  ↳ Manquant : [Ressource]`) clearly communicates failing prerequisites at a glance.
**Action:** When a composite CLI status check fails, pair the overall status banner with explicit indented diagnostic items explaining exactly what failed or is missing.
