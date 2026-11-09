## 2026-03-30 - Text-based capacity progress indicator in CLI workflows

**Learning:** Terminal-based user interfaces often display quota information purely as raw numerical values. Providing a dual representation with both numerical remaining/total capacity and a visual text progress meter (e.g. `[■■■□□□□□□□]`) improves comprehension at a glance for screen reader users and visual CLI users alike.
**Action:** When displaying limited capacity or finite slots in CLI applications, combine fraction counts with accessible unicode progress blocks (`■`/`□`).

## 2026-03-30 - Itemized system precondition checks in CLI diagnostics

**Learning:** CLI status utilities that condense multi-check validations into a single binary status indicator (e.g., `BASTION VERROUILLÉ` vs `DÉSYNCHRONISATION DÉTECTÉE`) force users to inspect source code or guess which precondition failed. Displaying an itemized checklist of each verified seal or subsystem with status badges (`ALIGNÉ ✅` vs `MANQUANT ⚠️`) provides immediate diagnostic clarity without requiring troubleshooting steps.
**Action:** Always itemize individual prerequisite checks alongside high-level system status summaries in CLI diagnostic tools.
