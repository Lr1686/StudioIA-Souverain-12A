import os
import log_event

def test_enregistrer_evenement_sanitizes_newlines_and_creates_dir(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    dirty_message = "Normal event\n[2026-03-30 00:00:00] [CRITICAL] Fake forged log entry\rInjected line"
    log_event.enregistrer_evenement(dirty_message)

    captured = capsys.readouterr()
    assert "\\n" in captured.out
    assert "\n[2026-03-30" not in captured.out

    log_file = "DATA/LOGS_SOUVERAINS/session_log.txt"
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        lines = f.readlines()

    # Verify log injection is prevented: single line output with escaped controls
    assert len(lines) == 1
    assert "Normal event\\n[2026-03-30 00:00:00] [CRITICAL] Fake forged log entry\\rInjected line" in lines[0]
