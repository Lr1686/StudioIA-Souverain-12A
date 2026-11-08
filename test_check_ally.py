import json
import check_ally


def test_initialiser_alliee_success(tmp_path, monkeypatch, capsys):
    test_config = tmp_path / "config_anastasia.json"
    data = {
        "alias": "Anastasia",
        "statut": "Légataire Souveraine",
        "frequence": "12_ALPHA",
        "origine": "MacBook Pro 2010"
    }
    test_config.write_text(json.dumps(data))

    check_ally.charger_config.cache_clear()
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(test_config))

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()
    assert "--- [ INITIALISATION ALLIÉE ] ---" in captured.out
    assert "ALIAS      : Anastasia" in captured.out
    assert "STATUT     : Légataire Souveraine" in captured.out
    assert "FRÉQUENCE  : 12_ALPHA" in captured.out
    assert "Souveraineté confirmée via MacBook Pro 2010" in captured.out


def test_charger_config_caching(tmp_path):
    test_config = tmp_path / "config_test.json"
    initial_data = {"alias": "Anastasia", "statut": "Légataire"}
    test_config.write_text(json.dumps(initial_data))

    check_ally.charger_config.cache_clear()
    config_first = check_ally.charger_config(str(test_config))
    assert config_first == initial_data

    # Modify the file on disk without clearing cache; cached value must return
    modified_data = {"alias": "Anastasia", "statut": "Modifie"}
    test_config.write_text(json.dumps(modified_data))

    config_cached = check_ally.charger_config(str(test_config))
    assert config_cached == initial_data
    assert config_cached is config_first

    # Clearing cache should now read updated data
    check_ally.charger_config.cache_clear()
    config_fresh = check_ally.charger_config(str(test_config))
    assert config_fresh == modified_data


def test_initialiser_alliee_missing_config(tmp_path, monkeypatch, capsys):
    missing_config = tmp_path / "missing_config.json"
    check_ally.charger_config.cache_clear()
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(missing_config))

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()
    assert "ERREUR : Le noyau d'identité est manquant." in captured.out
