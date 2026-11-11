import log_event


def test_enregistrer_evenement_succes(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    result = log_event.enregistrer_evenement("Événement de test standard")
    assert result is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Événement de test standard" in captured.out

    assert test_log.exists()
    content = test_log.read_text(encoding="utf-8")
    assert "Événement de test standard" in content


def test_enregistrer_evenement_crlf_log_injection(tmp_path, monkeypatch):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Attempt log injection with newline and forged timestamp/message
    malicious_msg = "Connexion réussie\n[2026-01-01 00:00:00] [FORGED] Accès admin accordé à l'attaquant\rInjection"
    result = log_event.enregistrer_evenement(malicious_msg)
    assert result is True

    content = test_log.read_text(encoding="utf-8")
    lines = [line for line in content.splitlines() if line.strip()]

    # Assert only 1 line was written, verifying CRLF injection is prevented
    assert len(lines) == 1
    assert "\n" not in lines[0]
    assert "\r" not in lines[0]
    assert "FORGED" in lines[0]


def test_enregistrer_evenement_invalid_inputs(tmp_path, monkeypatch, capsys):
    test_log = tmp_path / "LOGS_SOUVERAINS" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    # Test non-string types
    assert log_event.enregistrer_evenement(12345) is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out

    assert log_event.enregistrer_evenement(None) is False
    assert log_event.enregistrer_evenement(["un", "message"]) is False

    # Test empty or whitespace-only strings
    assert log_event.enregistrer_evenement("") is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out

    assert log_event.enregistrer_evenement("   \t  \n ") is False


def test_enregistrer_evenement_directory_creation(tmp_path, monkeypatch):
    nested_dir = tmp_path / "nested" / "logs" / "audit"
    test_log = nested_dir / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(test_log))

    assert not nested_dir.exists()
    result = log_event.enregistrer_evenement("Premier message dans dossier imbriqué")
    assert result is True
    assert nested_dir.exists()
    assert test_log.exists()
