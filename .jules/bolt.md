## 2026-03-30 - Stream line counting vs JSON deserialization for record tracking

**Learning:** In `gestion_pionniers.py`, JSON Lines records were being fully deserialized (`json.loads`) into memory dicts when only record count was required for capacity checks and ID generation. Replacing `json.loads` parsing with streaming line counting (`sum(1 for line in f if line.strip())`) achieves ~4x speedup and O(1) memory usage.
**Action:** Avoid deep deserialization of JSON/JSONL when only line or record counts are needed for ID generation or limit validation.

## 2026-03-30 - `len(os.listdir())` vs `os.scandir()` generator for counting

**Learning:** Using `sum(1 for _ in os.scandir(path))` in a pure Python generator for counting directory items is ~30% slower than `len(os.listdir(path))` on small to medium directories because `os.listdir` constructs the list in C, avoiding Python bytecode iteration overhead.
**Action:** Use `len(os.listdir(path))` when only counting directory items unless directory size is extremely large (>100k files).
