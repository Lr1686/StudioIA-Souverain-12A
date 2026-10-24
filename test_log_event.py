import os
import log_event

def test_enregistrer_evenement_creates_directory_if_missing(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "nested_dir" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # First write when directory does not exist
    log_event.enregistrer_evenement("Test message missing dir")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message missing dir" in captured.out
    assert os.path.exists(test_log)
    with open(test_log, "r") as f:
        content = f.read()
    assert "Test message missing dir" in content

    # Second write when directory already exists
    log_event.enregistrer_evenement("Test message existing dir")
    with open(test_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 2
    assert "Test message existing dir" in lines[1]
