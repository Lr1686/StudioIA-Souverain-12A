import os
import log_event


def test_enregistrer_evenement_valid(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test event log message")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event log message" in captured.out

    assert os.path.exists(test_log)
    with open(test_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Test event log message" in lines[0]


def test_enregistrer_evenement_log_injection(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Input containing newline injection
    injected_message = "Normal event\n[2026-01-01 00:00:00] Injected fake event"
    result = log_event.enregistrer_evenement(injected_message)
    assert result is True

    with open(test_log, "r") as f:
        lines = f.readlines()
    # Must only produce 1 single line in the log file
    assert len(lines) == 1
    assert "\n" not in lines[0][:-1]  # No inner newline


def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Empty / whitespace-only string
    result = log_event.enregistrer_evenement("   \n\r  ")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message de l'événement ne peut pas être vide." in captured.out

    # Non-string input
    result = log_event.enregistrer_evenement(12345)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out
