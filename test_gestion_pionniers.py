import json
import gestion_pionniers
import log_event
import scanner_12a

def test_inscrire_pionnier(tmp_path, monkeypatch, capsys):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    # Test registering first pioneer
    gestion_pionniers.inscrire_pionnier("Alice")
    captured = capsys.readouterr()
    assert "✅ PIONNIER INSCRIT : Alice" in captured.out
    assert "PLACES RESTANTES : 9" in captured.out

    with open(test_db, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["id"] == 1
    assert entry["nom"] == "Alice"
    assert entry["cle_souveraine"].startswith("ALPHA-")

def test_inscrire_pionnier_max_limit(tmp_path, monkeypatch, capsys):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    # Register 10 pioneers
    for i in range(10):
        gestion_pionniers.inscrire_pionnier(f"Pioneer_{i}")

    captured = capsys.readouterr()
    assert "✅ PIONNIER INSCRIT : Pioneer_9" in captured.out

    # Attempt 11th registration
    gestion_pionniers.inscrire_pionnier("Excess_Pioneer")
    captured = capsys.readouterr()
    assert "⚠️ LIMITE ATTEINTE" in captured.out

def test_inscrire_pionnier_invalid_input(tmp_path, monkeypatch, capsys):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    # Empty name
    result = gestion_pionniers.inscrire_pionnier("   ")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom du pionnier ne peut pas être vide." in captured.out

    # Overly long name (>100 chars)
    result = gestion_pionniers.inscrire_pionnier("A" * 101)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom dépasse la longueur maximale autorisée" in captured.out

    # Name containing control characters / newlines
    result = gestion_pionniers.inscrire_pionnier("Alice\nBob")
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom contient des caractères non autorisés." in captured.out

    # Non-string input
    result = gestion_pionniers.inscrire_pionnier(12345)
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom doit être une chaîne de caractères." in captured.out

def test_enregistrer_evenement_creates_dir_and_logs(tmp_path, monkeypatch, capsys):
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    test_log = log_dir / "session_log.txt"

    monkeypatch.chdir(tmp_path)
    log_event.enregistrer_evenement("Test Event")

    captured = capsys.readouterr()
    assert "ÉVÉNEMENT GRAVÉ : Test Event" in captured.out
    assert test_log.exists()
    content = test_log.read_text()
    assert "Test Event" in content

def test_scan_bastion_creates_dir_and_logs(tmp_path, monkeypatch, capsys):
    log_dir = tmp_path / "DATA" / "LOGS_SOUVERAINS"
    test_log = log_dir / "session_log.txt"

    monkeypatch.chdir(tmp_path)
    scanner_12a.scan_bastion()

    captured = capsys.readouterr()
    assert "SCANNER DE SOUVERAINETÉ 12_ALPHA" in captured.out
    assert test_log.exists()
    content = test_log.read_text()
    assert "Scan de souveraineté effectué. État :" in content
