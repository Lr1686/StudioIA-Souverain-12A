import os
import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Test log message")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test log message" in captured.out

    assert os.path.exists(test_log)
    with open(test_log, "r", encoding="utf-8") as f:
        content = f.read()
    assert "] Test log message\n" in content

def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non string input
    assert log_event.enregistrer_evenement(123) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty / whitespace input
    assert log_event.enregistrer_evenement("   ") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Newlines / log injection input
    assert log_event.enregistrer_evenement("Message\n[2026-01-01 00:00:00] Fake log entry") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères non autorisés." in captured.out

    # Overly long message
    long_msg = "A" * (log_event.MAX_LOG_LENGTH + 1)
    assert log_event.enregistrer_evenement(long_msg) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out
