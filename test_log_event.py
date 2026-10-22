import os
import log_event

def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    res = log_event.enregistrer_evenement("Éveil réussi")
    assert res is True
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Éveil réussi" in captured.out

    assert test_log.exists()
    with open(test_log, "r") as f:
        content = f.read()
    assert "Éveil réussi" in content

def test_enregistrer_evenement_sanitization(tmp_path, monkeypatch):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Injection with newlines and control characters
    log_event.enregistrer_evenement("Ligne 1\nLigne 2\r\n[FAKE LOG] Admin logged in")

    with open(test_log, "r") as f:
        lines = f.readlines()

    # Should be exactly one log entry (one line)
    assert len(lines) == 1
    assert "\n" not in lines[0][:-1]  # No embedded newlines before the final newline
    assert "Ligne 1 Ligne 2  [FAKE LOG] Admin logged in" in lines[0]

def test_enregistrer_evenement_invalid_input(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Non-string
    assert log_event.enregistrer_evenement(12345) is False
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in capsys.readouterr().out

    # Empty / whitespace
    assert log_event.enregistrer_evenement("   ") is False
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in capsys.readouterr().out

    # Exceeding MAX_LOG_LENGTH
    assert log_event.enregistrer_evenement("A" * 501) is False
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in capsys.readouterr().out
