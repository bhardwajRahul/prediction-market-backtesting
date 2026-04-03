from __future__ import annotations

from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from pmxt_local.config import LocalProcessingConfig
from pmxt_local.processor import RelayHourProcessor
from pmxt_local.processor import materialize_filtered_hour


def _make_config(tmp_path: Path) -> LocalProcessingConfig:
    filtered_root = tmp_path / "filtered"
    tmp_root = tmp_path / "tmp"
    filtered_root.mkdir(parents=True, exist_ok=True)
    tmp_root.mkdir(parents=True, exist_ok=True)
    return LocalProcessingConfig(
        filtered_root=filtered_root,
        tmp_root=tmp_root,
        filtered_materialization_workers=1,
    )


def test_hour_processor_writes_filtered_artifacts(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    raw_path = tmp_path / "polymarket_orderbook_2026-03-21T12.parquet"
    pq.write_table(
        pa.table(
            {
                "market_id": [
                    "condition-a",
                    "condition-a",
                    "condition-a",
                    "condition-b",
                ],
                "update_type": [
                    "book_snapshot",
                    "price_change",
                    "trade",
                    "price_change",
                ],
                "data": [
                    '{"token_id":"token-yes","seq":1}',
                    '{"token_id":"token-yes","seq":2}',
                    '{"token_id":"token-yes","seq":3}',
                    '{"token_id":"token-no","seq":4}',
                ],
            }
        ),
        raw_path,
    )

    result = RelayHourProcessor(config).process_hour(
        "polymarket_orderbook_2026-03-21T12.parquet",
        raw_path,
        write_processed=False,
    )

    assert {
        (artifact.condition_id, artifact.token_id, artifact.row_count)
        for artifact in result.artifacts
    } == {
        ("condition-a", "token-yes", 2),
        ("condition-b", "token-no", 1),
    }
    assert pq.read_table(
        config.filtered_root
        / "condition-a"
        / "token-yes"
        / "polymarket_orderbook_2026-03-21T12.parquet"
    ).to_pylist() == [
        {
            "update_type": "book_snapshot",
            "data": '{"token_id":"token-yes","seq":1}',
        },
        {
            "update_type": "price_change",
            "data": '{"token_id":"token-yes","seq":2}',
        },
    ]


def test_hour_processor_can_stream_filtered_batches_without_writing_artifacts(
    tmp_path: Path,
) -> None:
    config = _make_config(tmp_path)
    raw_path = tmp_path / "polymarket_orderbook_2026-03-21T15.parquet"
    pq.write_table(
        pa.table(
            {
                "market_id": [
                    "condition-a",
                    "condition-a",
                    "condition-b",
                    "condition-b",
                ],
                "update_type": [
                    "book_snapshot",
                    "price_change",
                    "price_change",
                    "trade",
                ],
                "data": [
                    '{"token_id":"token-yes","seq":1}',
                    '{"token_id":"token-yes","seq":2}',
                    '{"token_id":"token-no","seq":3}',
                    '{"token_id":"token-no","seq":4}',
                ],
            }
        ),
        raw_path,
    )

    captured_batches: list[pa.RecordBatch] = []
    result = RelayHourProcessor(config).process_hour(
        "polymarket_orderbook_2026-03-21T15.parquet",
        raw_path,
        skip_filtered=True,
        write_processed=False,
        batch_sink=lambda hour, batch: captured_batches.append(batch),
    )

    assert result.artifacts == []
    assert result.total_filtered_rows == 3
    assert result.filtered_group_count == 2
    assert sum(batch.num_rows for batch in captured_batches) == 3
    assert all("relay_row_index" in batch.schema.names for batch in captured_batches)


def test_materialized_filtered_hour_preserves_original_row_order(
    tmp_path: Path,
) -> None:
    processed_path = tmp_path / "processed.parquet"
    filtered_path = tmp_path / "filtered" / "condition-a" / "token-yes" / "hour.parquet"
    filtered_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(
        pa.table(
            {
                "market_id": [
                    "condition-a",
                    "condition-b",
                    "condition-a",
                    "condition-b",
                    "condition-a",
                ],
                "token_id": [
                    "token-yes",
                    "token-no",
                    "token-yes",
                    "token-no",
                    "token-yes",
                ],
                "update_type": [
                    "book_snapshot",
                    "price_change",
                    "price_change",
                    "price_change",
                    "price_change",
                ],
                "data": [
                    '{"token_id":"token-yes","seq":1}',
                    '{"token_id":"token-no","seq":2}',
                    '{"token_id":"token-yes","seq":3}',
                    '{"token_id":"token-no","seq":4}',
                    '{"token_id":"token-yes","seq":5}',
                ],
            }
        ),
        processed_path,
        row_group_size=2,
    )

    materialize_filtered_hour(
        processed_path,
        filtered_path,
        condition_id="condition-a",
        token_id="token-yes",
    )

    assert pq.read_table(filtered_path).to_pylist() == [
        {
            "update_type": "book_snapshot",
            "data": '{"token_id":"token-yes","seq":1}',
        },
        {
            "update_type": "price_change",
            "data": '{"token_id":"token-yes","seq":3}',
        },
        {
            "update_type": "price_change",
            "data": '{"token_id":"token-yes","seq":5}',
        },
    ]
