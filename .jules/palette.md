## 2026-03-30 - Text-based capacity progress indicator in CLI workflows

**Learning:** Terminal-based user interfaces often display quota information purely as raw numerical values. Providing a dual representation with both numerical remaining/total capacity and a visual text progress meter (e.g. `[■■■□□□□□□□]`) improves comprehension at a glance for screen reader users and visual CLI users alike.
**Action:** When displaying limited capacity or finite slots in CLI applications, combine fraction counts with accessible unicode progress blocks (`■`/`□`).

## 2026-03-30 - Itemized visual status feedback in CLI diagnostic scanners

**Learning:** Aggregate diagnostic checks (such as an overall pass/fail status) leave users uncertain about which exact requirement succeeded or failed when troubleshooting issues. Providing itemized visual indicators (`ALIGNÉ ✅` / `MANQUANT (target) ❌`) along with graceful platform fallbacks reduces cognitive friction and eliminates guesswork in terminal environments.
**Action:** For CLI diagnostic tools and integrity scanners, present each checked condition as an individual labeled line with clear status indicators and specific missing targets.
