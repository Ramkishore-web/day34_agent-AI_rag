
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_STORAGE_DIR = Path("data") / "runs"


def _validate_run_id(run_id: str) -> None:
    """Prevent unsafe file names."""
    if not run_id or not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
        raise ValueError("Invalid run_id")


def persist_run(
    run_id: str,
    payload: dict[str, Any],
    storage_dir: str | Path = DEFAULT_STORAGE_DIR,
) -> Path:
    """
    Persist a workflow snapshot as JSON.

    Writes atomically so an interrupted write is less likely
    to leave a partially written result file.
    """
    _validate_run_id(run_id)

    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")

    directory = Path(storage_dir)
    directory.mkdir(parents=True, exist_ok=True)

    destination = directory / f"{run_id}.json"
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False,
            suffix=".tmp",
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)

            json.dump(
                {
                    "run_id": run_id,
                    "payload": payload,
                },
                temporary_file,
                ensure_ascii=False,
                indent=2,
            )
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, destination)

    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    return destination


def load_run(
    run_id: str,
    storage_dir: str | Path = DEFAULT_STORAGE_DIR,
) -> dict[str, Any] | None:
    """Load a saved workflow snapshot, or return None if absent."""
    _validate_run_id(run_id)

    source = Path(storage_dir) / f"{run_id}.json"

    if not source.exists():
        return None

    with source.open("r", encoding="utf-8") as file:
        record = json.load(file)

    if not isinstance(record, dict):
        raise ValueError("Stored run record is invalid")

    if record.get("run_id") != run_id:
        raise ValueError("Stored run_id does not match requested run")

    if not isinstance(record.get("payload"), dict):
        raise ValueError("Stored run payload is invalid")

    return record
