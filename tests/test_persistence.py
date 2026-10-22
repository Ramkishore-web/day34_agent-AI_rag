
import json

import pytest

from src.workflow import persistence


def test_persist_and_load_run(tmp_path):
    payload = {"status": "success", "answer": "Research completed"}

    saved_path = persistence.persist_run("run_001", payload, tmp_path)
    loaded = persistence.load_run("run_001", tmp_path)

    assert saved_path.exists()
    assert loaded == {"run_id": "run_001", "payload": payload}


def test_load_missing_run_returns_none(tmp_path):
    assert persistence.load_run("missing_run", tmp_path) is None


@pytest.mark.parametrize("run_id", ["", "../unsafe", "run/one", "run one"])
def test_invalid_run_id_is_rejected(tmp_path, run_id):
    with pytest.raises(ValueError, match="Invalid run_id"):
        persistence.persist_run(run_id, {}, tmp_path)


def test_non_dictionary_payload_is_rejected(tmp_path):
    with pytest.raises(TypeError, match="payload must be a dictionary"):
        persistence.persist_run("run_002", ["invalid"], tmp_path)


def test_persistence_failure_cleans_temporary_file(tmp_path, monkeypatch):
    def fail_replace(source, destination):
        raise OSError("simulated disk failure")

    monkeypatch.setattr(persistence.os, "replace", fail_replace)

    with pytest.raises(OSError, match="simulated disk failure"):
        persistence.persist_run("run_failure", {"status": "success"}, tmp_path)

    assert not (tmp_path / "run_failure.json").exists()
    assert list(tmp_path.glob("*.tmp")) == []


def test_invalid_stored_json_is_rejected(tmp_path):
    file_path = tmp_path / "run_bad.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        persistence.load_run("run_bad", tmp_path)


def test_stored_run_id_mismatch_is_rejected(tmp_path):
    file_path = tmp_path / "run_003.json"
    file_path.write_text(
        json.dumps({"run_id": "other_run", "payload": {}}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="does not match"):
        persistence.load_run("run_003", tmp_path)
