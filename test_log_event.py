import os
import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    # Log first event (parent directory does not exist yet)
    log_event.enregistrer_evenement("Test Event 1")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test Event 1" in captured.out

    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        content = f.read()
    assert "Test Event 1" in content

    # Log second event (parent directory already exists)
    log_event.enregistrer_evenement("Test Event 2")
    with open(log_file, "r") as f:
        lines = f.readlines()
    assert len(lines) == 2
    assert "Test Event 2" in lines[1]
