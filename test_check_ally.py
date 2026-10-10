import json
import check_ally

def test_initialiser_alliee_success(tmp_path, monkeypatch, capsys):
    config_file = tmp_path / "config_anastasia.json"
    config_data = {
        "alias": "Anastasia",
        "statut": "Légataire Souveraine",
        "frequence": "12_ALPHA",
        "origine": "MacBook Pro 2010"
    }
    config_file.write_text(json.dumps(config_data))

    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(config_file))
    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "--- [ INITIALISATION ALLIÉE ] ---" in captured.out
    assert "ALIAS      : Anastasia" in captured.out
    assert "STATUT     : Légataire Souveraine" in captured.out
    assert "FRÉQUENCE  : 12_ALPHA" in captured.out
    assert "Souveraineté confirmée via MacBook Pro 2010" in captured.out

def test_initialiser_alliee_missing(tmp_path, monkeypatch, capsys):
    missing_file = tmp_path / "missing.json"
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(missing_file))

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "ERREUR : Le noyau d'identité est manquant." in captured.out
