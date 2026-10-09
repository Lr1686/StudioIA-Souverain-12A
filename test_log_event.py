import os
import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test event log message")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event log message" in captured.out

    assert os.path.exists(test_log)
    with open(test_log, "r") as f:
        content = f.read()
    assert "] Test event log message\n" in content

def test_enregistrer_evenement_validation_errors(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty / whitespace-only input
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Overly long message (>500 chars)
    assert log_event.enregistrer_evenement("A" * 501) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale" in captured.out

    # Log injection with newline character
    assert log_event.enregistrer_evenement("Log line 1\n[2026-01-01 00:00:00] Fake Log") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés ou des sauts de ligne." in captured.out
