import json
import check_ally

def test_initialiser_alliee_succes(tmp_path, monkeypatch, capsys):
    config_file = tmp_path / "config_anastasia.json"
    config_data = {
        "alias": "TestAlias",
        "statut": "TestStatut",
        "frequence": "TestFreq",
        "origine": "TestOrigine"
    }
    config_file.write_text(json.dumps(config_data), encoding="utf-8")

    monkeypatch.setattr("os.path.exists", lambda path: True if path == "DATA/config_anastasia.json" else False)

    # Mock open for DATA/config_anastasia.json
    orig_open = open
    def mock_open(file, *args, **kwargs):
        if file == "DATA/config_anastasia.json":
            return orig_open(config_file, *args, **kwargs)
        return orig_open(file, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "--- [ INITIALISATION ALLIÉE ] ---" in captured.out
    assert "ALIAS      : TestAlias" in captured.out
    assert "STATUT     : TestStatut" in captured.out
    assert "Souveraineté confirmée via TestOrigine" in captured.out

def test_initialiser_alliee_fichier_manquant(monkeypatch, capsys):
    monkeypatch.setattr("os.path.exists", lambda path: False)

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "⚠️ ERREUR : Le noyau d'identité est manquant (DATA/config_anastasia.json)." in captured.out
