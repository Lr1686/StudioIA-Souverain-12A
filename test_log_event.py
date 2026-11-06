import log_event


def test_enregistrer_evenement_success(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "subdir" / "session_log.txt"
    monkeypatch.setattr(log_event, "LOG_PATH", str(log_file))

    res = log_event.enregistrer_evenement("Test log message")
    assert res is True

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test log message" in captured.out

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert content.endswith("Test log message\n")
    assert "[" in content and "]" in content


def test_enregistrer_evenement_non_string(capsys):
    res = log_event.enregistrer_evenement(12345)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message doit être une chaîne de caractères." in captured.out


def test_enregistrer_evenement_empty(capsys):
    res = log_event.enregistrer_evenement("   ")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message ne peut pas être vide." in captured.out


def test_enregistrer_evenement_max_length(capsys):
    res = log_event.enregistrer_evenement("A" * 501)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message dépasse la longueur maximale autorisée" in captured.out


def test_enregistrer_evenement_log_injection_newlines(capsys):
    # Attempt log forging with newline injection
    malicious = "Normal message\n[2026-04-13 00:00:00] Injected fake log entry"
    res = log_event.enregistrer_evenement(malicious)
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle ou sauts de ligne non autorisés." in captured.out


def test_enregistrer_evenement_control_chars(capsys):
    # Attempt control character injection (e.g. carriage return or backspace)
    res = log_event.enregistrer_evenement("Normal\rFake")
    assert res is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le message contient des caractères de contrôle ou sauts de ligne non autorisés." in captured.out
