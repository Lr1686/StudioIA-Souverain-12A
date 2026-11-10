import json
import check_ally


def test_initialiser_alliee_success(tmp_path, monkeypatch, capsys):
    config_file = tmp_path / "config_anastasia.json"
    config_file.write_text(
        json.dumps(
            {
                "alias": "Anastasia",
                "statut": "Légataire Souveraine",
                "frequence": "12_ALPHA",
                "origine": "MacBook Pro 2010",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(config_file))

    success = check_ally.initialiser_alliee()
    assert success is True

    captured = capsys.readouterr()
    assert "--- [ INITIALISATION ALLIÉE ] ---" in captured.out
    assert "ALIAS      : Anastasia" in captured.out
    assert "STATUT     : Légataire Souveraine" in captured.out
    assert "FRÉQUENCE  : 12_ALPHA" in captured.out
    assert "Souveraineté confirmée via MacBook Pro 2010" in captured.out


def test_initialiser_alliee_missing_config(tmp_path, monkeypatch, capsys):
    non_existent_file = tmp_path / "does_not_exist.json"
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(non_existent_file))

    success = check_ally.initialiser_alliee()
    assert success is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le noyau d'identité est manquant" in captured.out
    assert str(non_existent_file) in captured.out
    assert (
        "💡 CONSEIL : Vérifiez l'existence du fichier de configuration" in captured.out
    )


def test_initialiser_alliee_corrupted_config(tmp_path, monkeypatch, capsys):
    corrupted_file = tmp_path / "corrupted.json"
    corrupted_file.write_text("{ broken json: true", encoding="utf-8")
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(corrupted_file))

    success = check_ally.initialiser_alliee()
    assert success is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le fichier de configuration" in captured.out
    assert "est corrompu ou illisible." in captured.out
    assert "💡 CONSEIL : Vérifiez la syntaxe JSON" in captured.out
