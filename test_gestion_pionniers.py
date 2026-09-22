import gestion_pionniers
from gestion_pionniers import inscrire_pionnier


def test_inscrire_pionnier_valide(tmp_path, monkeypatch):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    result = inscrire_pionnier("Alice")
    assert result is True
    assert test_db.exists()

    with open(test_db, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        assert "Alice" in lines[0]


def test_inscrire_pionnier_nom_vide(tmp_path, monkeypatch):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    assert inscrire_pionnier("") is False
    assert inscrire_pionnier("   ") is False
    assert not test_db.exists()


def test_inscrire_pionnier_nom_trop_long(tmp_path, monkeypatch):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    nom_long = "A" * 51
    assert inscrire_pionnier(nom_long) is False
    assert not test_db.exists()


def test_inscrire_pionnier_non_string(tmp_path, monkeypatch):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))

    assert inscrire_pionnier(12345) is False  # type: ignore
    assert not test_db.exists()


def test_inscrire_pionnier_limite_atteinte(tmp_path, monkeypatch):
    test_db = tmp_path / "registre_pionniers.json"
    monkeypatch.setattr(gestion_pionniers, "DB_PATH", str(test_db))
    monkeypatch.setattr(gestion_pionniers, "MAX_PIONNIERS", 2)

    assert inscrire_pionnier("Pionnier 1") is True
    assert inscrire_pionnier("Pionnier 2") is True
    assert inscrire_pionnier("Pionnier 3") is False
