import log_event


def test_enregistrer_evenement(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "test_session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    message = "Test sovereign event"
    log_event.enregistrer_evenement(message)

    captured = capsys.readouterr()
    assert f"🔱 ÉVÉNEMENT GRAVÉ : {message}\n" in captured.out

    assert test_log.exists()
    content = test_log.read_text(encoding="utf-8")
    assert content.endswith(f"] {message}\n")
    assert content.startswith("[")
