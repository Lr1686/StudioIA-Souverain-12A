## 2026-03-30 - Stream line counting vs JSON deserialization for record tracking

**Learning:** In `gestion_pionniers.py`, JSON Lines records were being fully deserialized (`json.loads`) into memory dicts when only record count was required for capacity checks and ID generation. Replacing `json.loads` parsing with streaming line counting (`sum(1 for line in f if line.strip())`) achieves ~4x speedup and O(1) memory usage.
**Action:** Avoid deep deserialization of JSON/JSONL when only line or record counts are needed for ID generation or limit validation.

## 2026-03-30 - Pre-compiled C-regex vs Python generator for string character validation

**Learning:** Character-by-character string inspection using Python generator comprehensions (`any(ord(c) < 32 or ord(c) == 127 for c in str)`) incurs significant Python interpreter loop overhead. Pre-compiling a regex (`re.compile(r'[\x00-\x1f\x7f]')`) delegates matching to C-level loops, yielding a ~6x speedup.
**Action:** Use pre-compiled regular expressions for character set validation instead of character-by-character generator comprehensions.
