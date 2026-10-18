# Palette's Journal - CLI UX & Accessibility Learnings

## 2026-03-30 - CLI Capacity Feedback & Proactive Input Prevention
**Learning:** In CLI interfaces, prompting users for input when an operation is guaranteed to fail due to capacity limits creates unnecessary frustration. Providing status feedback (current usage and remaining capacity) before requesting input improves clarity and user experience.
**Action:** Always check resource capacity and display available spots before prompting for user input in interactive CLI scripts.
