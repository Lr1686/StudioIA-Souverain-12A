import log_event

def test_enregistrer_evenement_sanitization(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test newline and carriage return sanitization (prevent log injection)
    log_event.enregistrer_evenement("Test\nLine2\rLine3")
    captured = capsys.readouterr()
    assert "Line2" in captured.out
    assert "\nLine2" not in captured.out

    # Test control characters stripping
    log_event.enregistrer_evenement("Test\x07Bell\x1bEsc")
    captured = capsys.readouterr()
    assert "TestBellEsc" in captured.out

    # Test length truncation
    long_msg = "A" * 600
    log_event.enregistrer_evenement(long_msg)
    captured = capsys.readouterr()
    assert "A" * 500 in captured.out
    assert "A" * 501 not in captured.out

def test_enregistrer_evenement_non_string(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    log_event.enregistrer_evenement(12345)
    captured = capsys.readouterr()
    assert "12345" in captured.out
