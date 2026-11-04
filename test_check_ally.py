import json
import check_ally


def test_initialiser_alliee_succes(tmp_path, monkeypatch, capsys):
    mock_config = tmp_path / "config_anastasia.json"
    mock_config.write_text(
        json.dumps({
            "alias": "Anastasia",
            "statut": "Légataire Souveraine",
            "frequence": "12_ALPHA",
            "origine": "MacBook Pro 2010"
        })
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("os.path.exists", lambda path: True if path == "DATA/config_anastasia.json" else False)

    # Use open patching for the target file
    original_open = open

    def fake_open(file, mode="r", *args, **kwargs):
        if file == "DATA/config_anastasia.json":
            return original_open(mock_config, mode, *args, **kwargs)
        return original_open(file, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "--- [ INITIALISATION ALLIÉE ] ---" in captured.out
    assert "ALIAS      : Anastasia" in captured.out
    assert "STATUT     : Légataire Souveraine" in captured.out
    assert "FRÉQUENCE  : 12_ALPHA" in captured.out
    assert "Souveraineté confirmée via MacBook Pro 2010 ✅" in captured.out


def test_initialiser_alliee_champs_manquants(tmp_path, monkeypatch, capsys):
    mock_config = tmp_path / "config_anastasia.json"
    mock_config.write_text(json.dumps({}))

    monkeypatch.setattr("os.path.exists", lambda path: True if path == "DATA/config_anastasia.json" else False)

    original_open = open

    def fake_open(file, mode="r", *args, **kwargs):
        if file == "DATA/config_anastasia.json":
            return original_open(mock_config, mode, *args, **kwargs)
        return original_open(file, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "ALIAS      : NON DÉFINI" in captured.out
    assert "STATUT     : NON DÉFINI" in captured.out
    assert "FRÉQUENCE  : NON DÉFINIE" in captured.out
    assert "Souveraineté confirmée via SOURCE INCONNUE ✅" in captured.out


def test_initialiser_alliee_fichier_manquant(monkeypatch, capsys):
    monkeypatch.setattr("os.path.exists", lambda path: False)

    check_ally.initialiser_alliee()
    captured = capsys.readouterr()

    assert "⚠️ ERREUR : Le noyau d'identité est manquant (DATA/config_anastasia.json)." in captured.out
    assert "💡 CONSEIL : Vérifiez que le fichier existe ou restaurez la configuration initiale." in captured.out
