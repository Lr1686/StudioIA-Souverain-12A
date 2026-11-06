import json
import check_ally


def test_initialiser_alliee_succes(tmp_path, monkeypatch, capsys):
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
    res = check_ally.initialiser_alliee()
    assert res is True

    captured = capsys.readouterr()
    assert "--- [ INITIALISATION ALLIÉE ] ---" in captured.out
    assert "ALIAS      : Anastasia" in captured.out
    assert "STATUT     : Légataire Souveraine" in captured.out
    assert "FRÉQUENCE  : 12_ALPHA" in captured.out
    assert "✅ Souveraineté confirmée via MacBook Pro 2010" in captured.out


def test_initialiser_alliee_fichier_manquant(tmp_path, monkeypatch, capsys):
    missing_config = tmp_path / "absent.json"
    monkeypatch.setattr(check_ally, "CONFIG_PATH", str(missing_config))

    res = check_ally.initialiser_alliee()
    assert res is False

    captured = capsys.readouterr()
    assert "⚠️ ERREUR : Le noyau d'identité est manquant" in captured.out
    assert str(missing_config) in captured.out
    assert "💡 CONSEIL" in captured.out
