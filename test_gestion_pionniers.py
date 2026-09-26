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

def test_inscrire_pionnier_invalid_and_sanitized_inputs(tmp_path, monkeypatch, capsys):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    # Empty name
    gestion_pionniers.inscrire_pionnier("   ")
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom du pionnier ne peut pas être vide." in captured.out

    # Non-string input
    gestion_pionniers.inscrire_pionnier(123)
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom doit être une chaîne de caractères." in captured.out

    # Overly long name
    gestion_pionniers.inscrire_pionnier("A" * 101)
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom dépasse la longueur maximale autorisée" in captured.out

    # Newline injection attempt
    gestion_pionniers.inscrire_pionnier("Bob\nInjected_Line")
    captured = capsys.readouterr()
    assert "✅ PIONNIER INSCRIT : Bob Injected_Line" in captured.out

    # Verify log file contains exactly 1 JSON line for Bob Injected_Line
    with open(test_db, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["nom"] == "Bob Injected_Line"
