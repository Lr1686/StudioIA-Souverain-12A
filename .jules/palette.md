## 2026-03-30 - Actionable Error Diagnostics for CLI Tools
**Learning:** For CLI status scanning scripts, outputting generic warning messages when checks fail leaves users guessing. Providing specific, component-level failure reasons makes the CLI far more actionable and intuitive.
**Action:** When a check or scan fails, explicitly print which items are missing or failing alongside the high-level warning status.
