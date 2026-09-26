import os
import json
import gestion_pionniers

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

def test_inscrire_pionnier_input_validation(tmp_path, monkeypatch, capsys):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    # Non-string input
    assert gestion_pionniers.inscrire_pionnier(12345) is False
    captured = capsys.readouterr()
    assert "ERREUR : Le nom doit être une chaîne de caractères" in captured.out

    # Empty string / Whitespace only
    assert gestion_pionniers.inscrire_pionnier("   ") is False
    captured = capsys.readouterr()
    assert "ERREUR : Le nom ne peut pas être vide" in captured.out

    # String too long (> 100 chars)
    long_name = "A" * 101
    assert gestion_pionniers.inscrire_pionnier(long_name) is False
    captured = capsys.readouterr()
    assert "ERREUR : Le nom ne peut pas dépasser 100 caractères" in captured.out

    # String with newline injection
    assert gestion_pionniers.inscrire_pionnier("Bob\nInjected_Pioneer") is False
    captured = capsys.readouterr()
    assert "ERREUR : Le nom ne peut pas contenir de sauts de ligne" in captured.out

    # Ensure no entries were written to DB for invalid inputs
    assert not os.path.exists(test_db)
