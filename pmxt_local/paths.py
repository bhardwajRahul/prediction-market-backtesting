from __future__ import annotations

from pathlib import Path

from pmxt_relay.storage import parse_archive_hour


def processed_relative_path(filename: str) -> Path:
    return Path(parse_archive_hour(filename).strftime("%Y/%m/%d")) / filename


def filtered_relative_path(condition_id: str, token_id: str, filename: str) -> Path:
    parse_archive_hour(filename)
    return Path(condition_id) / token_id / filename
