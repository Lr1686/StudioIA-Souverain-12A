import os
import log_event

def test_enregistrer_evenement_actual_func(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "session_log.txt"
    os.makedirs(tmp_path, exist_ok=True)

    # Run log_event with log_path patched
    original_open = open
    def mock_open(file, mode="r", *args, **kwargs):
        if "session_log.txt" in str(file):
            return original_open(log_file, mode, *args, **kwargs)
        return original_open(file, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    log_event.enregistrer_evenement("Test event message")
    captured = capsys.readouterr()
    assert "🔱 ÉVÉNEMENT GRAVÉ : Test event message" in captured.out

    with open(log_file, "r") as f:
        content = f.read()
    assert "Test event message\n" in content
