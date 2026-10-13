import log_event

def test_enregistrer_evenement_normal(tmp_path, capsys):
    log_file = tmp_path / "LOGS" / "test_log.txt"
    log_event.enregistrer_evenement("Normal event message", log_path=str(log_file))

    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Normal event message" in captured.out

    with open(log_file, "r") as f:
        content = f.read()
    assert "Normal event message" in content

def test_enregistrer_evenement_sanitization(tmp_path, capsys):
    log_file = tmp_path / "LOGS" / "test_log.txt"
    malicious_input = "Event\n[2026-01-01 00:00:00] FAKE CRITICAL LOG\r\nAttack"

    log_event.enregistrer_evenement(malicious_input, log_path=str(log_file))

    with open(log_file, "r") as f:
        lines = f.readlines()

    # Injection should be sanitized into a single line
    assert len(lines) == 1
    assert "FAKE CRITICAL LOG" in lines[0]
    assert "\n" not in lines[0][:-1]
