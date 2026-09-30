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

def test_inscrire_pionnier_validation(tmp_path, monkeypatch, capsys):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    # 1. Non-string name
    gestion_pionniers.inscrire_pionnier(12345)
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom du pionnier doit être une chaîne de caractères." in captured.out

    # 2. Empty or whitespace-only name
    gestion_pionniers.inscrire_pionnier("   ")
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom du pionnier ne peut pas être vide." in captured.out

    # 3. Overly long name (> 100 characters)
    gestion_pionniers.inscrire_pionnier("A" * 101)
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le nom du pionnier est trop long" in captured.out

    # Verify no entries were written
    assert not os.path.exists(test_db)
