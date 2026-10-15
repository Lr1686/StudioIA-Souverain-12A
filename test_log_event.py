import log_event

def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "sub_folder" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    log_event.enregistrer_evenement("Test message")

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test message" in captured.out

    assert test_log.exists()
    content = test_log.read_text()
    assert "Test message" in content
