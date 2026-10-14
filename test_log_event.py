import os
import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test event logging when directory does not exist initially
    assert not os.path.exists(test_log.parent)
    log_event.enregistrer_evenement("Test message 1")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message 1" in captured.out
    assert os.path.exists(test_log)

    with open(test_log, "r") as f:
        content = f.read()
    assert "Test message 1" in content

    # Test appending second message when directory already exists
    log_event.enregistrer_evenement("Test message 2")
    with open(test_log, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 2
    assert "Test message 2" in lines[1]
