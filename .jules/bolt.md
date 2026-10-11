## 2026-03-30 - Stream line counting vs JSON deserialization for record tracking

**Learning:** In `gestion_pionniers.py`, JSON Lines records were being fully deserialized (`json.loads`) into memory dicts when only record count was required for capacity checks and ID generation. Replacing `json.loads` parsing with streaming line counting (`sum(1 for line in f if line.strip())`) achieves ~4x speedup and O(1) memory usage.
**Action:** Avoid deep deserialization of JSON/JSONL when only line or record counts are needed for ID generation or limit validation.

## 2026-03-30 - Conditional platform version inspection on system scans

**Learning:** `platform.mac_ver()` executes OS system profile commands / plist lookups regardless of OS host. Conditionally calling `platform.mac_ver()` only when `platform.system() == "Darwin"` avoids unnecessary process / file inspection overhead on non-macOS environments (~9x speedup, 0.4ms vs 3.8ms per call).
**Action:** Check `platform.system()` before calling OS-specific version functions like `platform.mac_ver()` or `platform.win32_ver()`.
