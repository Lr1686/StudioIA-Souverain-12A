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
import json
import os
import pytest
import gestion_pionniers


def test_inscrire_pionnier_creation_and_limit(tmp_path, monkeypatch, capsys):
    test_data_dir = tmp_path / "DATA"
    test_db_path = test_data_dir / "KNOWLEDGE_BASE" / "registre_pionniers.json"

    monkeypatch.setattr(gestion_pionniers, "DATA_DIR", str(test_data_dir))
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db_path))

    # Inscrire un pionnier
    gestion_pionniers.inscrire_pionnier("Alice")

    assert test_db_path.exists()

    with open(test_db_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["nom"] == "Alice"
        assert data["id"] == 1
        assert "ALPHA-" in data["cle_souveraine"]

    captured = capsys.readouterr()
    assert "PIONNIER INSCRIT : Alice" in captured.out


def test_get_safe_path_security(tmp_path, monkeypatch):
    test_data_dir = tmp_path / "DATA"
    test_data_dir.mkdir()

    monkeypatch.setattr(gestion_pionniers, "DATA_DIR", str(test_data_dir))

    safe_file = test_data_dir / "sub" / "file.txt"
    assert gestion_pionniers._get_safe_path(str(safe_file)) == os.path.abspath(safe_file)

    unsafe_file = tmp_path / "outside.txt"
    with pytest.raises(ValueError, match="Sécurité: tentative d'accès en dehors du répertoire autorisé."):
        gestion_pionniers._get_safe_path(str(unsafe_file))
