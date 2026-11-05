import json
import check_ally


def test_initialiser_alliee_success(tmp_path, monkeypatch, capsys):
    mock_config = tmp_path / "config_anastasia.json"
    mock_config.write_text(
        json.dumps(
            {
                "alias": "Anastasia",
                "statut": "Légataire Souveraine",
                "frequence": "12_ALPHA",
                "origine": "MacBook Pro 2010",
            }
        )
    )
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(mock_config))

    result = check_ally.initialiser_alliee()
    assert result is True
    captured = capsys.readouterr()
    assert "--- [ INITIALISATION ALLIÉE ] ---" in captured.out
    assert "ALIAS      : Anastasia" in captured.out
    assert "STATUT     : Légataire Souveraine" in captured.out
    assert "FRÉQUENCE  : 12_ALPHA" in captured.out
    assert "✅ Souveraineté confirmée via MacBook Pro 2010" in captured.out


def test_initialiser_alliee_missing_config(tmp_path, monkeypatch, capsys):
    non_existent = tmp_path / "missing.json"
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(non_existent))

    result = check_ally.initialiser_alliee()
    assert result is False
    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le noyau d'identité est manquant" in captured.out
    assert str(non_existent) in captured.out


def test_initialiser_alliee_partial_config(tmp_path, monkeypatch, capsys):
    mock_config = tmp_path / "config_partial.json"
    mock_config.write_text(json.dumps({"alias": "TestAlly"}))
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(mock_config))

    result = check_ally.initialiser_alliee()
    assert result is True
    captured = capsys.readouterr()
    assert "ALIAS      : TestAlly" in captured.out
    assert "STATUT     : Inconnu" in captured.out
    assert "FRÉQUENCE  : Non assignée" in captured.out
    assert "✅ Souveraineté confirmée via Origine indéterminée" in captured.out
