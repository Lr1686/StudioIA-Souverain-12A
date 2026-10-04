## 2026-03-30 - Stream line counting vs JSON deserialization for record tracking

**Learning:** In `gestion_pionniers.py`, JSON Lines records were being fully deserialized (`json.loads`) into memory dicts when only record count was required for capacity checks and ID generation. Replacing `json.loads` parsing with streaming line counting (`sum(1 for line in f if line.strip())`) achieves ~4x speedup and O(1) memory usage.
**Action:** Avoid deep deserialization of JSON/JSONL when only line or record counts are needed for ID generation or limit validation.

## 2026-10-04 - `datetime.isoformat` vs `strftime` for standard ISO timestamp formatting

**Learning:** In Python, calling `datetime.datetime.now().isoformat(sep=" ", timespec="seconds")` is ~2.7x faster than `datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")` because `isoformat` is implemented natively in C in CPython without string format specification parsing overhead.
**Action:** Use `isoformat(sep=" ", timespec="seconds")` when formatting timestamps in standard ISO date-time formats (`YYYY-MM-DD HH:MM:SS`).
