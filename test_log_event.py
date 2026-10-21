import log_event

def test_enregistrer_evenement_existing_directory(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "LOGS" / "session_log.txt"
    log_file.parent.mkdir()

    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    log_event.enregistrer_evenement("Test Log Message")

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test Log Message" in captured.out
    assert log_file.exists()
    content = log_file.read_text()
    assert "Test Log Message" in content


def test_enregistrer_evenement_auto_create_directory(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "NON_EXISTING_DIR" / "session_log.txt"

    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    log_event.enregistrer_evenement("Auto Dir Test")

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Auto Dir Test" in captured.out
    assert log_file.exists()
    content = log_file.read_text()
    assert "Auto Dir Test" in content
