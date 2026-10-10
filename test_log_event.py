import os
import log_event

def test_enregistrer_evenement_sanitization(tmp_path):
    log_file = tmp_path / "session_log.txt"

    # Multiline message with log injection attempt
    injection_msg = "Normal Log\n[2026-03-30 00:00:00] INJECTED_LOG: System compromised\r[2026-03-30 00:00:01] Extra"

    log_event.enregistrer_evenement(injection_msg, log_path=str(log_file))

    assert log_file.exists()
    lines = log_file.read_text().splitlines()

    # Check that the log entry is strictly on a single line (no newline injection)
    assert len(lines) == 1
    assert "\n" not in lines[0]
    assert "\r" not in lines[0]
    assert "Normal Log [2026-03-30 00:00:00] INJECTED_LOG: System compromised [2026-03-30 00:00:01] Extra" in lines[0]
