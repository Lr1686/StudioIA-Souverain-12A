import os
import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Test Event Message")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test Event Message" in captured.out

    with open(test_log, "r") as f:
        content = f.read()
    assert "Test Event Message" in content

def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string input
    result = log_event.enregistrer_evenement(12345)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    # Empty message
    result = log_event.enregistrer_evenement("   ")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    # Overly long message (>500 chars)
    result = log_event.enregistrer_evenement("A" * 501)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out

    # Control characters / newline injection attack
    result = log_event.enregistrer_evenement("Fake Log\n[2026-01-01 00:00:00] Admin access granted")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle" in captured.out
