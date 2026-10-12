import log_event

def test_enregistrer_evenement(tmp_path, capsys):
    log_file = tmp_path / "sub_dir" / "session_log.txt"
    message = "Test event message"

    log_event.enregistrer_evenement(message, log_path=str(log_file))

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event message" in captured.out

    assert log_file.exists()
    content = log_file.read_text()
    assert "Test event message" in content
    assert content.startswith("[")
