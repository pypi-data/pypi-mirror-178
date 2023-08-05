import datetime
import json
import logging

import mock
import numpy as np
import pandas as pd
import pytest
import responses
from freezegun import freeze_time

from gantry.exceptions import GantryBatchCreationException, GantryLoggingDataTypeError
from gantry.logger import client
from gantry.logger.constants import BatchType, UploadFileType
from gantry.logger.stores import BaseLogStore
from gantry.logger.types import DataLink, DataLinkElement

CURRENT_TIME, CURRENT_TIME_STR = datetime.datetime(2032, 5, 23, 0, 0, 0), "2032-05-23T00:00:00"
FUTURE_TIME = datetime.datetime(2042, 5, 23, 0, 0, 0)
SOME_TIME, SOME_TIME_STR = datetime.datetime(2022, 5, 10, 17, 50, 32), "2022-05-10T17:50:32"
ANOTHER_TIME, ANOTHER_TIME_STR = datetime.datetime(2022, 5, 11, 17, 50, 32), "2022-05-11T17:50:32"
HOST = "http://test-api"


class TestLogStore(BaseLogStore):
    def __init__(self):
        self.logs = []
        self.status = False

    def log_batch(self, application, events) -> None:
        self.logs.append({"application": application, "events": events})

    def ping(self) -> bool:
        return self.status


@pytest.fixture(scope="function")
def log_store():
    return TestLogStore()


@pytest.fixture(scope="function")
def cli_obj(log_store):
    return client.Gantry(log_store=log_store, environment="test", logging_level="DEBUG")


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize(
    ["sort", "timestamps", "record_count", "expected"],
    [
        (False, [3, 4, 5, 1, 2], 10, [(0, 3), (1, 4), (2, 5), (3, 1), (4, 2)]),
        (True, [3, 4, 5, 1, 2], 10, [(3, 1), (4, 2), (0, 3), (1, 4), (2, 5)]),
        (False, ["b", "a", "c"], 100, [(0, "b"), (1, "a"), (2, "c")]),
        (True, ["b", "a", "c"], 100, [(1, "a"), (0, "b"), (2, "c")]),
        (
            True,
            None,
            4,
            [
                (0, CURRENT_TIME),
                (1, CURRENT_TIME),
                (2, CURRENT_TIME),
                (3, CURRENT_TIME),
            ],
        ),
        (
            False,
            None,
            4,
            [
                (0, CURRENT_TIME),
                (1, CURRENT_TIME),
                (2, CURRENT_TIME),
                (3, CURRENT_TIME),
            ],
        ),
    ],
)
def test_create_timestamp_idx(sort, timestamps, record_count, expected):
    assert list(client._create_timestamp_idx(sort, timestamps, record_count)) == expected


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@pytest.mark.parametrize("feedback_version", [None, 5, "1.2.3"])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_build_feedback_event(mock_uuid, feedback_version, timestamp):
    mock_uuid.return_value = "123abc"
    assert client._build_feedback_event(
        context={"foo": "bar"},
        application="barbaz",
        feedback_id={"a": 10},
        feedback={"b": 20},
        feedback_version=feedback_version,
        timestamp=timestamp,
        batch_id="ABCD1234",
    ) == {
        "batch_id": "ABCD1234",
        "event_id": "123abc",
        "feedback": {"b": 20},
        "feedback_id": "2a30f5f3b7d1a97cb6132480b992d984",
        "feedback_id_inputs": {"a": 10},
        "log_timestamp": CURRENT_TIME_STR,
        "metadata": {"feedback_version": feedback_version, "foo": "bar", "func_name": "barbaz"},
        "timestamp": SOME_TIME_STR if timestamp else CURRENT_TIME_STR,
    }


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize(
    ["feedback_keys", "feedback_id"],
    [
        (None, None),
        (["some-input"], None),
        (None, {"id": "yes"}),
    ],
)
@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_build_prediction_event(mock_uuid, timestamp, feedback_keys, feedback_id):
    mock_uuid.return_value = "123abc"
    assert client._build_prediction_event(
        context={"foo": "bar"},
        env="test",
        inputs={"some-input": "a-input"},
        outputs={"some-output": "a-output"},
        application="barbaz",
        version="1.2.3",
        feedback_keys=feedback_keys,
        ignore_inputs=["some-other-input"],
        batch_id="ABCD1234",
        feedback_id=feedback_id,
        tags={"this-is": "a-tag"},
        custom_timestamp=timestamp,
    ) == {
        "batch_id": "ABCD1234",
        "event_id": "123abc",
        "feedback_id": "1f972d1df351de3ce35a787c89faad29"
        if feedback_id
        else "afd8cf8889da593bcb98dae5c86101ca",
        "inputs": {"some-input": "a-input"},
        "log_timestamp": CURRENT_TIME_STR,
        "metadata": {
            "feedback_keys": feedback_keys,
            "foo": "bar",
            "version": "1.2.3",
            "ignore_inputs": ["some-other-input"],
            "provided_feedback_id": feedback_id,
            "func_name": "barbaz",
        },
        "timestamp": SOME_TIME_STR if timestamp else CURRENT_TIME_STR,
        "outputs": {"some-output": "a-output"},
        "tags": {"env": "test", "this-is": "a-tag"},
    }

    with pytest.raises(GantryLoggingDataTypeError):
        client._build_prediction_event(
            context={"foo": "bar"},
            env="test",
            inputs={"some-invalid-input": ["invalid", {"invalid": True}]},
            outputs={"some-output": "a-output"},
            application="barbaz",
            version="1.2.3",
            feedback_keys=[],
            ignore_inputs=[],
            batch_id="ABCD1234",
            feedback_id=feedback_id,
            tags={"this-is": "a-tag"},
            custom_timestamp=timestamp,
        )


def test_ping_fail(cli_obj):
    cli_obj.log_store.status = False
    assert not cli_obj.ping()


def test_ping_success(cli_obj):
    cli_obj.log_store.status = True
    assert cli_obj.ping()


@pytest.mark.parametrize("application", [10, None, 10.5, b"some binary string"])
def test_log_feedback_event_invalid_name(application, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback_event(
        application=application,
        feedback_id={"A": 100},
        feedback={"value": "bar"},
        feedback_version=10,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_id", [10, None, 10.5, ["a", "list"], b"something"])
def test_log_feedback_event_invalid_feedback_id(feedback_id, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback_event(
        application="foobar",
        feedback_id=feedback_id,
        feedback={"value": "bar"},
        feedback_version=10,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback", [10, None, 10.5, ["a", "list"], b"something"])
def test_log_feedback_event_invalid_feedback(feedback, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback_event(
        application="foobar",
        feedback_id={"value": "bar"},
        feedback=feedback,
        feedback_version=10,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_version", [b"a-version", 10.5, {"version": "yes"}, [10]])
def test_log_feedback_event_invalid_feedback_version(feedback_version, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback_event(
        application="foobar",
        feedback_id={"value": "bar"},
        feedback={"value": "foo"},
        feedback_version=feedback_version,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("timestamp", ["some-timestamp", 10, "2020-10-10"])
def test_log_feedback_event_invalid_timestamp(timestamp, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback_event(
        application="foobar",
        feedback_id={"value": "bar"},
        feedback={"value": "foo"},
        feedback_version=10,
        timestamp=timestamp,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("timestamp", [FUTURE_TIME])
def test_log_feedback_event_future_timestamp(timestamp, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback_event(
        application="foobar",
        feedback_id={"value": "bar"},
        feedback={"value": "foo"},
        feedback_version=10,
        timestamp=timestamp,
    )

    # Assert that there were no logs written, since the dates are in the future.
    assert len(cli_obj.log_store.logs) == 0


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@pytest.mark.parametrize("feedback_version", [None, "1.2.3", 10])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_feedback_event(mock_uuid, feedback_version, timestamp, tags, cli_obj):
    mock_uuid.return_value = "12345"
    cli_obj.log_feedback_event(
        application="foobar",
        feedback_id={"A": 100},
        feedback={"value": "bar"},
        feedback_version=feedback_version,
        timestamp=timestamp,
        tags=tags,
    )
    assert cli_obj.log_store.logs == [
        {
            "events": [
                {
                    "batch_id": None,
                    "event_id": "12345",
                    "feedback": {"value": "bar"},
                    "feedback_id": "5dd14615efeb2d086e519ed35efd3f73",
                    "feedback_id_inputs": {"A": 100},
                    "log_timestamp": CURRENT_TIME_STR,
                    "metadata": {
                        "environment": tags["env"] if tags else "test",
                        "feedback_version": feedback_version,
                        "func_name": "foobar",
                    },
                    "timestamp": SOME_TIME_STR if timestamp else CURRENT_TIME_STR,
                }
            ],
            "application": "foobar",
        },
    ]


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_feedback_event_sample_rate_0_5(mock_uuid, timestamp):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.4):
        gantry.log_feedback_event(
            application="foobar",
            feedback_id={"A": 100},
            feedback={"value": "bar"},
            feedback_version=10,
            timestamp=timestamp,
            sample_rate=0.5,
        )

    log_store.log.assert_called_once()


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_feedback_event_sample_rate_0_5_none(mock_uuid, timestamp):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")
    with mock.patch("random.random", return_value=0.6):
        mock_uuid.return_value = "12345"
        gantry.log_feedback_event(
            application="foobar",
            feedback_id={"A": 100},
            feedback={"value": "bar"},
            feedback_version=10,
            timestamp=timestamp,
            sample_rate=0.5,
        )

    log_store.log.assert_not_called()


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_feedback_event_sample_rate_0(mock_uuid, timestamp):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.4):
        mock_uuid.return_value = "12345"
        gantry.log_feedback_event(
            application="foobar",
            feedback_id={"A": 100},
            feedback={"value": "bar"},
            feedback_version=10,
            timestamp=timestamp,
            sample_rate=0.0,
        )

    log_store.log.assert_not_called()


@pytest.mark.parametrize("application", [10, None, 10.5, b"some binary string"])
def test_log_prediction_event_invalid_name(application, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_prediction_event(
        application=application,
        inputs={"A": 100},
        outputs={"value": "bar"},
        version=10,
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("inputs", [[10, 20], 10, None, 10.5, ("A", 100)])
def test_log_prediction_event_invalid_inputs(inputs, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_prediction_event(
        application="some-name",
        inputs=inputs,
        outputs={"value": "bar"},
        version=10,
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("version", [[10, 20], 10.5, {"version": 10}])
def test_log_prediction_event_invalid_version(version, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_prediction_event(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version=version,
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_keys", [[10, 20], 10.5, ("a", "b", "c")])
def test_log_prediction_event_invalid_feedback_keys(feedback_keys, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_prediction_event(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        feedback_keys=feedback_keys,
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize(
    "ignore_inputs", [[10, 20], [b"something", "binary"], ["bar", 10.5], [10, "foo"], 10, 10.5]
)
def test_log_prediction_event_invalid_ignore_inputs(ignore_inputs, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_prediction_event(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        ignore_inputs=ignore_inputs,
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_id", [[10, 20], ["foo"], 10, 10.5])
def test_log_prediction_event_invalid_feedback_id(feedback_id, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_prediction_event(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        feedback_keys=["A"],
        ignore_inputs=["A"],
        feedback_id=feedback_id,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("timestamp", [[], "some-timestamp", 10, "2020-10-10"])
def test_log_prediction_event_invalid_timestamp(timestamp, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_prediction_event(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        feedback_keys=["A"],
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=timestamp,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@pytest.mark.parametrize(
    ["feedback_keys", "feedback_id"],
    [
        (["A"], None),
        (None, {"A": 100}),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_prediction_event(mock_uuid, feedback_keys, feedback_id, timestamp, tags, cli_obj):
    mock_uuid.return_value = "12345"
    cli_obj.log_prediction_event(
        application="foobar",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        feedback_keys=feedback_keys,
        ignore_inputs=["A"],
        feedback_id=feedback_id,
        timestamp=timestamp,
        tags=tags,
    )
    assert cli_obj.log_store.logs == [
        {
            "events": [
                {
                    "batch_id": None,
                    "event_id": "12345",
                    "feedback_id": "5dd14615efeb2d086e519ed35efd3f73",
                    "inputs": {},
                    "log_timestamp": CURRENT_TIME_STR,
                    "metadata": {
                        "environment": tags["env"] if tags else "test",
                        "feedback_keys": ["A"] if feedback_keys else None,
                        "func_name": "foobar",
                        "ignore_inputs": ["A"],
                        "provided_feedback_id": {"A": 100} if feedback_id else None,
                        "version": "a.b.c",
                    },
                    "outputs": {"value": "bar"},
                    "tags": tags if tags else {"env": "test"},
                    "timestamp": CURRENT_TIME_STR if not timestamp else SOME_TIME_STR,
                }
            ],
            "application": "foobar",
        },
    ]


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@pytest.mark.parametrize(
    ["feedback_keys", "feedback_id"],
    [
        (["A"], None),
        (None, {"A": 100}),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_prediction_event_sample_rate_0_5(mock_uuid, feedback_keys, feedback_id, timestamp):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.4):
        mock_uuid.return_value = "12345"
        gantry.log_prediction_event(
            application="foobar",
            inputs={"A": 100},
            outputs={"value": "bar"},
            version="a.b.c",
            feedback_keys=feedback_keys,
            ignore_inputs=["A"],
            feedback_id=feedback_id,
            timestamp=timestamp,
            sample_rate=0.5,
        )

    log_store.log.assert_called_once()


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@pytest.mark.parametrize(
    ["feedback_keys", "feedback_id"],
    [
        (["A"], None),
        (None, {"A": 100}),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_prediction_event_sample_rate_0_5_none(
    mock_uuid, feedback_keys, feedback_id, timestamp
):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        mock_uuid.return_value = "12345"
        gantry.log_prediction_event(
            application="foobar",
            inputs={"A": 100},
            outputs={"value": "bar"},
            version="a.b.c",
            feedback_keys=feedback_keys,
            ignore_inputs=["A"],
            feedback_id=feedback_id,
            timestamp=timestamp,
            sample_rate=0.5,
        )

    log_store.log.assert_not_called()


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@pytest.mark.parametrize(
    ["feedback_keys", "feedback_id"],
    [
        (["A"], None),
        (None, {"A": 100}),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_prediction_event_sample_rate_0(mock_uuid, feedback_keys, feedback_id, timestamp):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        mock_uuid.return_value = "12345"
        gantry.log_prediction_event(
            application="foobar",
            inputs={"A": 100},
            outputs={"value": "bar"},
            version="a.b.c",
            feedback_keys=feedback_keys,
            ignore_inputs=["A"],
            feedback_id=feedback_id,
            timestamp=timestamp,
            sample_rate=0.0,
        )

    log_store.log.assert_not_called()


@pytest.mark.parametrize("application", [10, None, 10.5, b"some binary string"])
def test_log_record_invalid_name(application, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application=application,
        feedback_id={"A": 100},
        feedback={"value": "bar"},
        feedback_version=10,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_id", [10, None, 10.5, ["a", "list"], b"something"])
def test_log_record_invalid_feedback_id(feedback_id, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="foobar",
        feedback_id=feedback_id,
        feedback={"value": "bar"},
        feedback_version=10,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback", [10, None, 10.5, ["a", "list"], b"something"])
def test_log_record_invalid_feedback(feedback, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="foobar",
        feedback_id={"value": "bar"},
        feedback=feedback,
        feedback_version=10,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize(
    "feedback_version", ["some-version", b"a-version", 10.5, {"version": "yes"}, [10]]
)
def test_log_record_invalid_feedback_version(feedback_version, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="foobar",
        feedback_id={"value": "bar"},
        feedback={"value": "foo"},
        feedback_version=feedback_version,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("timestamp", ["some-timestamp", 10, "2020-10-10"])
def test_log_record_invalid_timestamp(timestamp, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="foobar",
        feedback_id={"value": "bar"},
        feedback={"value": "foo"},
        feedback_version=10,
        timestamp=timestamp,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("inputs", [[10, 20], 10, 10.5, ("A", 100)])
def test_log_record_invalid_inputs(inputs, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="some-name",
        inputs=inputs,
        outputs={"value": "bar"},
        version=10,
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("version", [[10, 20], 10.5, {"version": 10}])
def test_log_record_invalid_version(version, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version=version,
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_keys", [[10, 20], 10.5, ("a", "b", "c")])
def test_log_record_invalid_feedback_keys(feedback_keys, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        feedback_keys=feedback_keys,
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize(
    "ignore_inputs", [[10, 20], [b"something", "binary"], ["bar", 10.5], [10, "foo"], 10, 10.5]
)
def test_log_record_invalid_ignore_inputs(ignore_inputs, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        ignore_inputs=ignore_inputs,
        feedback_id={"A": 100},
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_id", [[10, 20], ["foo"], 10, 10.5])
def test_log_record_invalid_feedback_id_for_prediction(feedback_id, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        feedback_keys=["A"],
        ignore_inputs=["A"],
        feedback_id=feedback_id,
        timestamp=SOME_TIME,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("feedback_id", ["foo", {"foo": "bar"}])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_record_valid_feedback_id_for_prediction(mock_uuid, feedback_id, cli_obj):
    mock_uuid.return_value = "12345"
    cli_obj.log_record(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        ignore_inputs=["B"],
        feedback_id=feedback_id,
        timestamp=SOME_TIME,
    )
    assert cli_obj.log_store.logs == [
        {
            "events": [
                {
                    "batch_id": None,
                    "event_id": "12345",
                    "inputs": {"A": 100},
                    "outputs": {"value": "bar"},
                    "tags": {"env": "test"},
                    "feedback_id": "42a5b7b99b3717d1eaeb72a6948dabc9"
                    if isinstance(feedback_id, dict)
                    else feedback_id,
                    "log_timestamp": CURRENT_TIME_STR,
                    "metadata": {
                        "environment": "test",
                        "func_name": "some-name",
                        "provided_feedback_id": feedback_id,
                        "version": "a.b.c",
                        "ignore_inputs": ["B"],
                        "feedback_keys": None,
                    },
                    "timestamp": SOME_TIME_STR,
                }
            ],
            "application": "some-name",
        },
    ]


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("feedback_id", ["foo", {"foo": "bar"}])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_record_valid_feedback_id_for_feedback(mock_uuid, feedback_id, cli_obj):
    mock_uuid.return_value = "12345"
    cli_obj.log_record(
        application="some-name",
        feedback={"A": 100},
        version="a.b.c",
        feedback_id=feedback_id,
        timestamp=SOME_TIME,
    )
    assert cli_obj.log_store.logs == [
        {
            "events": [
                {
                    "batch_id": None,
                    "event_id": "12345",
                    "feedback": {"A": 100},
                    "feedback_id": "42a5b7b99b3717d1eaeb72a6948dabc9"
                    if isinstance(feedback_id, dict)
                    else feedback_id,
                    "feedback_id_inputs": feedback_id,
                    "log_timestamp": CURRENT_TIME_STR,
                    "metadata": {
                        "environment": "test",
                        "func_name": "some-name",
                        "feedback_version": "a.b.c",
                    },
                    "timestamp": SOME_TIME_STR,
                }
            ],
            "application": "some-name",
        },
    ]


@pytest.mark.parametrize("timestamp", [[], "some-timestamp", 10, "2020-10-10"])
def test_log_record_invalid_timestamp_for_prediction(timestamp, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_record(
        application="some-name",
        inputs={"A": 100},
        outputs={"value": "bar"},
        version="a.b.c",
        feedback_keys=["A"],
        ignore_inputs=["A"],
        feedback_id={"A": 100},
        timestamp=timestamp,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_prediction_and_feedback_event(mock_uuid, timestamp, tags, cli_obj):
    mock_uuid.return_value = "12345"
    cli_obj._log_prediction_and_feedback_event(
        application="foobar",
        version="a.b.c",
        inputs={"A": 100},
        outputs={"value": "bar"},
        feedback={"value": "potato"},
        timestamp=timestamp,
        tags=tags,
    )

    assert cli_obj.log_store.logs == [
        {
            "events": [
                {
                    "batch_id": None,
                    "event_id": "12345",
                    "feedback": {"value": "potato"},
                    "inputs": {"A": 100},
                    "outputs": {"value": "bar"},
                    "tags": tags if tags else {"env": "test"},
                    "feedback_id": "d751713988987e9331980363e24189ce",
                    "feedback_id_inputs": {},
                    "log_timestamp": CURRENT_TIME_STR,
                    "metadata": {
                        "environment": tags["env"] if tags else "test",
                        "feedback_version": "a.b.c",
                        "func_name": "foobar",
                        "provided_feedback_id": None,
                        "version": "a.b.c",
                        "ignore_inputs": None,
                        "feedback_keys": None,
                    },
                    "timestamp": SOME_TIME_STR if timestamp else CURRENT_TIME_STR,
                }
            ],
            "application": "foobar",
        },
    ]


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_prediction_and_feedback_event_sample_rate_0_5(mock_uuid, timestamp):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.4):
        mock_uuid.return_value = "12345"
        gantry._log_prediction_and_feedback_event(
            application="foobar",
            version="a.b.c",
            inputs={"A": 100},
            outputs={"value": "bar"},
            feedback={"value": "potato"},
            timestamp=timestamp,
            sample_rate=0.5,
        )

    log_store.log.assert_called_once()


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_prediction_and_feedback_event_sample_rate_0_5_none(mock_uuid, timestamp):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        mock_uuid.return_value = "12345"
        gantry._log_prediction_and_feedback_event(
            application="foobar",
            version="a.b.c",
            inputs={"A": 100},
            outputs={"value": "bar"},
            feedback={"value": "potato"},
            timestamp=timestamp,
            sample_rate=0.5,
        )

    log_store.log.assert_not_called()


@pytest.mark.parametrize("timestamp", [None, SOME_TIME])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_prediction_and_feedback_event_sample_rate_0(mock_uuid, timestamp):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        mock_uuid.return_value = "12345"
        gantry._log_prediction_and_feedback_event(
            application="foobar",
            version="a.b.c",
            inputs={"A": 100},
            outputs={"value": "bar"},
            feedback={"value": "potato"},
            timestamp=timestamp,
            sample_rate=0.0,
        )

    log_store.log.assert_not_called()


@pytest.mark.parametrize("application", [10, None, 10.5, b"some binary string"])
def test_log_feedback_invalid_name(application, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback(
        application=application,
        feedback_ids=[{"A": 100}],
        feedbacks=[{"value": "bar"}],
        feedback_version=10,
        timestamps=[SOME_TIME],
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_ids", [[10], 10, None, 10.5])
def test_log_feedback_invalid_feedback_id(feedback_ids, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback(
        application="foobar",
        feedback_ids=feedback_ids,
        feedbacks=[{"value": "bar"}],
        feedback_version=10,
        timestamps=[SOME_TIME],
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedbacks", [10, None, 10.5, (1, 2)])
def test_log_feedback_invalid_feedback(feedbacks, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback(
        application="foobar",
        feedback_ids=[{"value": "bar"}],
        feedbacks=feedbacks,
        feedback_version=10,
        timestamps=[SOME_TIME],
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_version", [{"this-is": 10}, ["1.2.3", "2.3.4"]])
def test_log_feedback_invalid_feedback_version(feedback_version, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback(
        application="foobar",
        feedback_ids=[{"value": "bar"}],
        feedbacks=[{"value": "foo"}],
        feedback_version=feedback_version,
        timestamps=[SOME_TIME],
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("timestamps", [[10], "some-timestamp", 10, ["2020-20-20", SOME_TIME]])
def test_log_feedback_invalid_timestamps(timestamps, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_feedback(
        application="foobar",
        feedback_ids=[{"value": "bar"}],
        feedbacks=[{"value": "foo"}],
        feedback_version=10,
        timestamps=timestamps,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize(
    "timestamps",
    [
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        None,
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize("random_error", [True, False])
@pytest.mark.parametrize(
    "feedbacks",
    [
        [{100: "some-value"}, {100: "some-other-value"}],
        pd.DataFrame({100: ["some-value", "some-other-value"]}),
        np.array([{100: "some-value"}, {100: "some-other-value"}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_feedback(mock_uuid, feedbacks, random_error, timestamps, sort, tags, cli_obj):
    if random_error:
        mock_uuid.side_effect = RuntimeError
    else:
        mock_uuid.return_value = "ABCD1234"
    rv = cli_obj.log_feedback(
        application="foobar",
        feedback_ids=[{"A": 100}, {"B": 200}],
        feedbacks=feedbacks,
        feedback_version=10,
        timestamps=timestamps,
        sort_on_timestamp=sort,
        as_batch=False,
        tags=tags,
    )
    assert rv is None
    events = [
        {
            "batch_id": None,
            "event_id": "ABCD1234",
            "feedback": {100: "some-other-value"},
            "feedback_id": "08b84280663845e83bbf82d297013a53",
            "feedback_id_inputs": {"B": 200},
            "log_timestamp": CURRENT_TIME_STR,
            "metadata": {
                "environment": tags["env"] if tags else "test",
                "feedback_version": 10,
                "func_name": "foobar",
            },
            "timestamp": SOME_TIME_STR if timestamps is not None else CURRENT_TIME_STR,
        },
        {
            "batch_id": None,
            "event_id": "ABCD1234",
            "feedback": {100: "some-value"},
            "feedback_id": "5dd14615efeb2d086e519ed35efd3f73",
            "feedback_id_inputs": {"A": 100},
            "log_timestamp": CURRENT_TIME_STR,
            "metadata": {
                "environment": tags["env"] if tags else "test",
                "feedback_version": 10,
                "func_name": "foobar",
            },
            "timestamp": ANOTHER_TIME_STR if timestamps is not None else CURRENT_TIME_STR,
        },
    ]

    if timestamps is not None:
        expected_events = [events[1], events[0]] if not sort else [events[0], events[1]]
    else:
        expected_events = [events[1], events[0]]

    if random_error:
        assert cli_obj.log_store.logs == []
    else:
        assert cli_obj.log_store.logs == [
            {
                "events": expected_events,
                "application": "foobar",
            }
        ]


@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize(
    "timestamps",
    [
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        None,
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize(
    "feedbacks",
    [
        [{100: "some-value"}, {100: "some-other-value"}],
        pd.DataFrame({100: ["some-value", "some-other-value"]}),
        np.array([{100: "some-value"}, {100: "some-other-value"}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_feedback_sample_rate_0_5(mock_uuid, feedbacks, timestamps, sort):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.4):
        mock_uuid.return_value = "ABCD1234"
        gantry.log_feedback(
            application="foobar",
            feedback_ids=[{"A": 100}, {"B": 200}],
            feedbacks=feedbacks,
            feedback_version=10,
            timestamps=timestamps,
            sort_on_timestamp=sort,
            sample_rate=0.5,
            as_batch=False,
        )

    log_store.log_batch.assert_called_once()


@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize(
    "timestamps",
    [
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        None,
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize(
    "feedbacks",
    [
        [{100: "some-value"}, {100: "some-other-value"}],
        pd.DataFrame({100: ["some-value", "some-other-value"]}),
        np.array([{100: "some-value"}, {100: "some-other-value"}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_feedback_sample_rate_0_5_none(mock_uuid, feedbacks, timestamps, sort, cli_obj):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        mock_uuid.return_value = "ABCD1234"
        gantry.log_feedback(
            application="foobar",
            feedback_ids=[{"A": 100}, {"B": 200}],
            feedbacks=feedbacks,
            feedback_version=10,
            timestamps=timestamps,
            sort_on_timestamp=sort,
            sample_rate=0.5,
            as_batch=False,
        )

    log_store.log_batch.assert_not_called()


@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize(
    "timestamps",
    [
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        None,
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize(
    "feedbacks",
    [
        [{100: "some-value"}, {100: "some-other-value"}],
        pd.DataFrame({100: ["some-value", "some-other-value"]}),
        np.array([{100: "some-value"}, {100: "some-other-value"}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_feedback_sample_rate_0_0(mock_uuid, feedbacks, timestamps, sort):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        mock_uuid.return_value = "ABCD1234"
        gantry.log_feedback(
            application="foobar",
            feedback_ids=[{"A": 100}, {"B": 200}],
            feedbacks=feedbacks,
            feedback_version=10,
            timestamps=timestamps,
            sort_on_timestamp=sort,
            sample_rate=0.0,
            as_batch=False,
        )

    log_store.log_batch.assert_not_called()


def test_log_feedback_mismatch_size(cli_obj):
    cli_obj.log_feedback(
        application="foobar",
        feedback_ids=[{"A": 100}],
        feedbacks=[{100: "some-value"}, {200: "some-other-value"}],
        feedback_version=10,
        timestamps=[ANOTHER_TIME, SOME_TIME],
        sort_on_timestamp=True,
        as_batch=False,
    )
    assert cli_obj.log_store.logs == []


@pytest.mark.parametrize("application", [10, None, 10.5, b"some binary string"])
def test_log_predictions_invalid_name(application, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_predictions(
        application=application,
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        feedback_keys=["A"],
        ignore_inputs=["A", "B"],
        version=10,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize(
    "inputs", [[10, {}], {"A": 100}, 10, None, 10.5, b"some binary string", (1, 2)]
)
def test_log_predictions_invalid_inputs(inputs, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_predictions(
        application="foobar",
        inputs=inputs,
        outputs=[{"C": 300}],
        feedback_keys=["A"],
        ignore_inputs=["A", "B"],
        version=10,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("outputs", [{"A": 100}, 10, None, 10.5, b"some binary string", (1, 2)])
def test_log_predictions_invalid_outputs(outputs, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=outputs,
        feedback_keys=["A"],
        ignore_inputs=["A", "B"],
        version=10,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("version", [{"A": 100}, 10.5, b"some binary string"])
def test_log_predictions_invalid_version(version, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        feedback_keys=["A"],
        ignore_inputs=["A", "B"],
        version=version,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_keys", [[{}], {"A": 100}, 10.5, b"some binary string"])
def test_log_predictions_invalid_feedback_keys(feedback_keys, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        feedback_keys=feedback_keys,
        ignore_inputs=["A", "B"],
        version=10,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("ignore_inputs", [[{}], {"A": 100}, 10.5, b"some binary string"])
def test_log_predictions_invalid_ignore_inputs(ignore_inputs, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        feedback_keys=["A"],
        ignore_inputs=ignore_inputs,
        version=10,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("feedback_ids", [[10], {"A": 100}, 10.5, b"some binary string"])
def test_log_predictions_invalid_feedback_ids(feedback_ids, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        ignore_inputs=["A", "B"],
        feedback_ids=feedback_ids,
        version=10,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@pytest.mark.parametrize("timestamps", [[10], "some-timestamp", 10, ["2020-20-20", SOME_TIME]])
def test_log_predictions_invalid_timestamps(timestamps, cli_obj, caplog):
    caplog.set_level(logging.ERROR, logger="gantry.client")
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        feedback_keys=["A"],
        ignore_inputs=["A", "B"],
        version=10,
        timestamps=timestamps,
        as_batch=False,
    )
    assert "Internal exception in Gantry client" in caplog.text
    assert "TypeError:" in caplog.text


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize(
    "timestamps",
    [
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        None,
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize("random_error", [True, False])
@pytest.mark.parametrize(
    "outputs",
    [
        [{"C": 300}, {"C": 303}],
        pd.DataFrame({"C": [300, 303]}),
        np.array([{"C": 300}, {"C": 303}]),
    ],
)
@pytest.mark.parametrize(
    "inputs",
    [
        [{"A": 100, "B": 200}, {"A": 101, "B": 202}],
        pd.DataFrame({"A": [100, 101], "B": [200, 202]}),
        np.array([{"A": 100, "B": 200}, {"A": 101, "B": 202}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_predictions(mock_uuid, inputs, outputs, random_error, timestamps, sort, tags, cli_obj):
    if random_error:
        mock_uuid.side_effect = RuntimeError
    else:
        mock_uuid.return_value = "ABCD1234"
    rv = cli_obj.log_predictions(
        application="foobar",
        inputs=inputs,
        outputs=outputs,
        feedback_keys=["A"],
        ignore_inputs=["B"],
        version=10,
        timestamps=timestamps,
        sort_on_timestamp=sort,
        as_batch=False,
        tags=tags,
    )
    assert rv is None

    events = [
        {
            "batch_id": None,
            "event_id": "ABCD1234",
            "feedback_id": "9e329293e022d6cdaafdec49b5f4fedc",
            "inputs": {"A": 101},
            "log_timestamp": CURRENT_TIME_STR,
            "metadata": {
                "environment": tags["env"] if tags else "test",
                "feedback_keys": ["A"],
                "func_name": "foobar",
                "ignore_inputs": ["B"],
                "provided_feedback_id": None,
                "version": 10,
            },
            "outputs": {"C": 303},
            "tags": tags if tags else {"env": "test"},
            "timestamp": SOME_TIME_STR if timestamps is not None else CURRENT_TIME_STR,
        },
        {
            "batch_id": None,
            "event_id": "ABCD1234",
            "feedback_id": "5dd14615efeb2d086e519ed35efd3f73",
            "inputs": {"A": 100},
            "log_timestamp": CURRENT_TIME_STR,
            "metadata": {
                "environment": tags["env"] if tags else "test",
                "feedback_keys": ["A"],
                "func_name": "foobar",
                "ignore_inputs": ["B"],
                "provided_feedback_id": None,
                "version": 10,
            },
            "outputs": {"C": 300},
            "tags": tags if tags else {"env": "test"},
            "timestamp": ANOTHER_TIME_STR if timestamps is not None else CURRENT_TIME_STR,
        },
    ]

    if timestamps is not None:
        expected_events = [events[1], events[0]] if not sort else [events[0], events[1]]
    else:
        expected_events = [events[1], events[0]]

    if random_error:
        assert cli_obj.log_store.logs == []
    else:
        assert cli_obj.log_store.logs == [
            {
                "events": expected_events,
                "application": "foobar",
            }
        ]


@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize(
    "timestamps",
    [
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        None,
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize(
    "outputs",
    [
        [{"C": 300}, {"C": 303}],
        pd.DataFrame({"C": [300, 303]}),
        np.array([{"C": 300}, {"C": 303}]),
    ],
)
@pytest.mark.parametrize(
    "inputs",
    [
        [{"A": 100, "B": 200}, {"A": 101, "B": 202}],
        pd.DataFrame({"A": [100, 101], "B": [200, 202]}),
        np.array([{"A": 100, "B": 200}, {"A": 101, "B": 202}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_predictions_sample_rate_0_5(mock_uuid, inputs, outputs, timestamps, sort, tags):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.4):
        mock_uuid.return_value = "ABCD1234"
        gantry.log_predictions(
            application="foobar",
            inputs=inputs,
            outputs=outputs,
            feedback_keys=["A"],
            ignore_inputs=["B"],
            version=10,
            timestamps=timestamps,
            sort_on_timestamp=sort,
            sample_rate=0.5,
            as_batch=False,
            tags=tags,
        )
    log_store.log_batch.assert_called_once()


@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize(
    "timestamps",
    [
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        None,
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize(
    "outputs",
    [
        [{"C": 300}, {"C": 303}],
        pd.DataFrame({"C": [300, 303]}),
        np.array([{"C": 300}, {"C": 303}]),
    ],
)
@pytest.mark.parametrize(
    "inputs",
    [
        [{"A": 100, "B": 200}, {"A": 101, "B": 202}],
        pd.DataFrame({"A": [100, 101], "B": [200, 202]}),
        np.array([{"A": 100, "B": 200}, {"A": 101, "B": 202}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_predictions_sample_rate_0_5_none(mock_uuid, inputs, outputs, timestamps, sort, tags):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        mock_uuid.return_value = "ABCD1234"
        gantry.log_predictions(
            application="foobar",
            inputs=inputs,
            outputs=outputs,
            feedback_keys=["A"],
            ignore_inputs=["B"],
            version=10,
            timestamps=timestamps,
            sort_on_timestamp=sort,
            sample_rate=0.5,
            as_batch=False,
            tags=tags,
        )
    log_store.log_batch.assert_not_called()


@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize(
    "timestamps",
    [
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        None,
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize(
    "outputs",
    [
        [{"C": 300}, {"C": 303}],
        pd.DataFrame({"C": [300, 303]}),
        np.array([{"C": 300}, {"C": 303}]),
    ],
)
@pytest.mark.parametrize(
    "inputs",
    [
        [{"A": 100, "B": 200}, {"A": 101, "B": 202}],
        pd.DataFrame({"A": [100, 101], "B": [200, 202]}),
        np.array([{"A": 100, "B": 200}, {"A": 101, "B": 202}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_log_predictions_sample_rate_0(mock_uuid, inputs, outputs, timestamps, sort, tags):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.1):
        mock_uuid.return_value = "ABCD1234"
        gantry.log_predictions(
            application="foobar",
            inputs=inputs,
            outputs=outputs,
            feedback_keys=["A"],
            ignore_inputs=["B"],
            version=10,
            timestamps=timestamps,
            sort_on_timestamp=sort,
            sample_rate=0.0,
            as_batch=False,
            tags=tags,
        )
    log_store.log_batch.assert_not_called()


def test_log_predictions_mismatch_size_inputs_outputs(cli_obj):
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}, {"C": 303}],
        feedback_keys=["A"],
        ignore_inputs=["B"],
        version=10,
        as_batch=False,
    )

    assert cli_obj.log_store.logs == []


def test_log_predictions_mismatch_size_timestamp(cli_obj):
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        feedback_keys=["A"],
        ignore_inputs=["B"],
        version=10,
        timestamps=[SOME_TIME, ANOTHER_TIME],
        as_batch=False,
    )

    assert cli_obj.log_store.logs == []


def test_log_predictions_mismatch_size_feedback_ids(cli_obj):
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        feedback_ids=[{"foo": "bar"}, {"bar": "baz"}],
        ignore_inputs=["B"],
        version=10,
        as_batch=False,
    )

    assert cli_obj.log_store.logs == []


def test_log_predictions_mismatch_size_version(cli_obj):
    cli_obj.log_predictions(
        application="foobar",
        inputs=[{"A": 100, "B": 200}],
        outputs=[{"C": 300}],
        feedback_keys=["A"],
        ignore_inputs=["B"],
        version=[1, 2, 3],
        as_batch=False,
    )

    assert cli_obj.log_store.logs == []


def test_batch_id_population_without_batch(initialized_gantry, tmp_path):
    inputs = [{"input1": i, "input2": 2} for i in range(20)]
    outputs = [i % 2 for i in range(20)]

    initialized_gantry.log_predictions(
        "simple_test", inputs, outputs, sort_on_timestamp=True, as_batch=False
    )

    log_path = tmp_path / "predictions" / "simple_test.log"
    assert log_path.exists()

    with log_path.open() as f:
        for i, line in enumerate(f):
            logged_ev = json.loads(line)
            assert i < 20  # Max of 20 events
            assert logged_ev["batch_id"] is None


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("version", ["0", 0, None])
@pytest.mark.parametrize("sort", [True, False])
@pytest.mark.parametrize("method", ["log_predictions", "log_records_prediction", "log_records"])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
@mock.patch("gantry.logger.client._batch_success_msg")
@mock.patch("gantry.logger.client._concurrent_upload_multipart_batch")
def test_log_predictions_as_batch(
    mock_upload, mock_batch_success, mock_uuid, version, sort, method, init_gantry_with_api
):
    mock_upload.return_value = [{"ETag": "working_etag", "PartNumber": 1}]

    if method == "log_records":
        size = 40
    else:
        size = 20
    mock_uuid.side_effect = [str(x) for x in range(size + 1)]

    inputs = [{"input1": i, "input2": 2} for i in range(20)]
    outputs = [i % 2 for i in range(20)]
    feedbacks = [{"val": i} for i in range(20)]

    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/ingest/file-preupload?filename=simple_test_{size}&num_parts=1&filetype=EVENTS",  # noqa
            json={
                "response": "ok",
                "upload_urls": ["http://test_url"],
                "upload_id": "10",
                "key": "x1234",
            },
        )
        resp.add(
            resp.POST,
            url=f"{HOST}/api/v1/ingest/file",
            json={"response": "ok", "batch_id": "hello_123"},
            headers={"Content-Type": "application/json"},
        )

        if method == "log_predictions":
            rv = init_gantry_with_api.log_predictions(
                "simple_test", inputs, outputs, version, sort_on_timestamp=sort, as_batch=True
            )

            assert rv == "hello_123"
        elif method == "log_records_prediction":
            rv = init_gantry_with_api.log_records(
                "simple_test",
                version,
                inputs=inputs,
                outputs=outputs,
                sort_on_timestamp=sort,
                as_batch=True,
            )

            assert rv == "hello_123"
        elif method == "log_records":
            rv = init_gantry_with_api.log_records(
                "simple_test",
                version,
                inputs=inputs,
                outputs=outputs,
                feedbacks=feedbacks,
                sort_on_timestamp=sort,
                as_batch=True,
            )

            assert rv == "hello_123"
        mock_batch_success.assert_called_once_with(
            "hello_123", "simple_test", init_gantry_with_api.get_client().log_store
        )


@pytest.mark.parametrize("version", ["0", 0, None])
@pytest.mark.parametrize("sort", [True, False])
@pytest.mark.parametrize("method", ["log_feedback", "log_records_feedback"])
@pytest.mark.parametrize("feedback_id", [{"value": "foo"}, "foo"])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
@mock.patch("gantry.logger.client._batch_success_msg")
@mock.patch("gantry.logger.client._concurrent_upload_multipart_batch")
def test_log_feedback_as_batch(
    mock_upload,
    mock_batch_success,
    mock_uuid,
    version,
    sort,
    method,
    init_gantry_with_api,
    feedback_id,
):
    size = 2
    mock_uuid.side_effect = [str(x) for x in range(size + 1)]
    feedbacks = [{"value": "foo"} for _ in range(size)]
    feedback_ids = [feedback_id for _ in range(size)]

    mock_upload.return_value = [{"ETag": "working_etag", "PartNumber": 1}]

    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/ingest/file-preupload?filename=simple_test_{size}&num_parts=1&filetype=EVENTS",  # noqa
            json={
                "response": "ok",
                "upload_urls": ["http://test_url"],
                "upload_id": "10",
                "key": "x1234",
            },
        )
        resp.add(
            resp.POST,
            f"{HOST}/api/v1/ingest/file",
            json={"response": "ok", "batch_id": "hello_123"},
            headers={"Content-Type": "application/json"},
        )

        if method == "log_feedback":
            rv = init_gantry_with_api.log_feedback(
                application="simple_test",
                feedback_ids=feedback_ids,
                feedbacks=feedbacks,
                feedback_version=version,
                sort_on_timestamp=sort,
                as_batch=True,
            )

            assert rv == "hello_123"
        elif method == "log_records_feedback":
            rv = init_gantry_with_api.log_records(
                "simple_test",
                version,
                feedback_ids=feedback_ids,
                feedbacks=feedbacks,
                sort_on_timestamp=sort,
                as_batch=True,
            )

            assert rv == "hello_123"
        mock_batch_success.assert_called_once_with(
            "hello_123", "simple_test", init_gantry_with_api.get_client().log_store
        )


@mock.patch("gantry.logger.event_builder.uuid.uuid4")
@mock.patch("gantry.logger.client._concurrent_upload_multipart_batch")
def test_batch_completion_fail(mock_upload, mock_uuid, init_gantry_with_api):
    mock_upload.return_value = [{"ETag": "working_etag", "PartNumber": 1}]

    size = 20
    inputs = [{"input1": i, "input2": 2} for i in range(size)]
    outputs = [i % 2 for i in range(size)]

    mock_uuid.side_effect = [str(x) for x in range(size + 1)]

    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/ingest/file-preupload?filename=simple_test_{size}&num_parts=1&filetype=EVENTS",  # noqa
            json={
                "response": "ok",
                "upload_urls": ["http://test_url"],
                "upload_id": "10",
                "key": "x1234",
            },
        )
        resp.add(
            resp.POST,
            f"{HOST}/api/v1/ingest/file",
            json={"response": "not-ok"},
            headers={"Content-Type": "application/json"},
        )

        with pytest.raises(GantryBatchCreationException):
            init_gantry_with_api.log_predictions(
                "simple_test", inputs, outputs, sort_on_timestamp=True, as_batch=True
            )


@mock.patch("gantry.logger.event_builder.uuid.uuid4")
def test_batch_preupload_fail(mock_uuid, init_gantry_with_api):
    size = 20
    inputs = [{"input1": i, "input2": 2} for i in range(size)]
    outputs = [i % 2 for i in range(size)]
    mock_uuid.side_effect = [str(x) for x in range(size + 1)]

    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/ingest/file-preupload?filename=simple_test_{size}&num_parts=1&filetype=EVENTS",  # noqa
            json={"response": "broken-return"},
        )

        with pytest.raises(GantryBatchCreationException):
            init_gantry_with_api.log_predictions(
                "simple_test", inputs, outputs, sort_on_timestamp=True, as_batch=True
            )


@pytest.mark.parametrize(
    ["inputs", "outputs", "feedbacks"],
    [
        ([{"A": 100}], None, [{"C": 100}]),
        (None, [{"A": 100}], [{"C": 100}]),
        (None, None, [{"C": 100}]),
        ([{"A": 100}], [{"C": 100}], None),
        ([{"A": 100}], None, None),
    ],
)
def test_log_predictions_and_feedbacks_no_preds_or_no_feedbacks(
    inputs, outputs, feedbacks, cli_obj, log_store
):
    cli_obj._log_predictions_and_feedbacks(
        application="foobar",
        version="2.0",
        inputs=inputs,
        outputs=outputs,
        feedback_keys=["A"],
        feedbacks=feedbacks,
    )

    assert log_store.logs == []


@pytest.mark.parametrize(
    ["inputs", "outputs", "feedbacks"],
    [
        ([{"A": 100}, {"A": 200}], [{"B": 100}], [{"B": 102}]),
        ([{"A": 100}, {"A": 200}], [{"B": 100}, {"B": 101}], [{"B": 102}]),
        ([{"A": 100}, {"A": 200}], [{"B": 100}, {"B": 101}], [{"B": 102}, {"B": 103}, {"B": 104}]),
        ([{"A": 100}], [{"B": 100}, {"B": 101}], [{"B": 102}, {"B": 103}, {"B": 104}]),
    ],
)
def test_log_predictions_and_feedbacks_size_mismatch(
    inputs, outputs, feedbacks, cli_obj, log_store
):
    cli_obj._log_predictions_and_feedbacks(
        application="foobar",
        version="2.0",
        inputs=inputs,
        outputs=outputs,
        feedback_keys=["A"],
        feedbacks=feedbacks,
    )

    assert log_store.logs == []


@pytest.mark.parametrize(
    "timestamps",
    [
        [],
        [SOME_TIME, ANOTHER_TIME],
        pd.DatetimeIndex([SOME_TIME, ANOTHER_TIME]),
    ],
)
def test_log_predictions_and_feedbacks_size_mismatch_timestamps(timestamps, cli_obj, log_store):
    cli_obj._log_predictions_and_feedbacks(
        application="foobar",
        version="2.0",
        inputs=[{"A": 100}],
        outputs=[{"B": 200}],
        feedback_keys=["A"],
        feedbacks=[{"A": 100}],
        timestamps=timestamps,
    )

    assert log_store.logs == []


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize(
    "timestamps",
    [
        None,
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize("version", ["0", 0, None])
@pytest.mark.parametrize("as_batch", [False, True])
@pytest.mark.parametrize(
    "test_feedbacks",
    [
        [{"A": 200}, {"A": 201}],
        pd.DataFrame.from_dict({"A": [200, 201]}),
        np.array([{"A": 200}, {"A": 201}]),
    ],
)
@pytest.mark.parametrize(
    "test_outputs",
    [
        [{"B": 300}, {"B": 301}],
        pd.DataFrame.from_dict({"B": [300, 301]}),
        np.array([{"B": 300}, {"B": 301}]),
    ],
)
@pytest.mark.parametrize(
    "test_inputs",
    [
        [{"A": 100}, {"A": 101}],
        pd.DataFrame.from_dict({"A": [100, 101]}),
        np.array([{"A": 100}, {"A": 101}]),
    ],
)
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
@mock.patch("gantry.logger.client.Gantry._upload_data_as_batch")
def test_log_predictions_and_feedbacks_df(
    mock_upload_data_as_batch,
    mock_uuid,
    test_inputs,
    test_outputs,
    test_feedbacks,
    as_batch,
    version,
    sort,
    timestamps,
    tags,
    cli_obj,
    log_store,
):
    mock_upload_data_as_batch.return_value = None
    mock_uuid.side_effect = ["ABCD1", "ABCD2", "ABCD3", "ABCD4"]
    cli_obj._log_predictions_and_feedbacks(
        application="foobar",
        version=version,
        inputs=test_inputs,
        outputs=test_outputs,
        feedback_keys=["A"],
        feedbacks=test_feedbacks,
        timestamps=timestamps,
        sort_on_timestamp=sort,
        as_batch=as_batch,
        tags=tags,
    )
    expected_tags = tags if tags else {"env": "test"}

    event_1 = {
        "event_id": "ABCD2" if not (sort and timestamps is not None) else "ABCD4",
        "log_timestamp": CURRENT_TIME_STR,
        "timestamp": ANOTHER_TIME_STR if timestamps is not None else CURRENT_TIME_STR,
        "metadata": {
            "environment": tags["env"] if tags else "test",
            "func_name": "foobar",
            "version": version,
            "feedback_keys": ["A"],
            "ignore_inputs": None,
            "provided_feedback_id": None,
            "feedback_version": version,
        },
        "inputs": {"A": 100},
        "outputs": {"B": 300},
        "feedback_id": "5dd14615efeb2d086e519ed35efd3f73",
        "tags": expected_tags,
        "batch_id": None,
        "feedback_id_inputs": {"A": 100},
        "feedback": {"A": 200},
    }

    event_2 = {
        "event_id": "ABCD4" if not (sort and timestamps is not None) else "ABCD2",
        "log_timestamp": CURRENT_TIME_STR,
        "timestamp": SOME_TIME_STR if timestamps is not None else CURRENT_TIME_STR,
        "metadata": {
            "environment": tags["env"] if tags else "test",
            "func_name": "foobar",
            "version": version,
            "feedback_keys": ["A"],
            "ignore_inputs": None,
            "provided_feedback_id": None,
            "feedback_version": version,
        },
        "inputs": {"A": 101},
        "outputs": {"B": 301},
        "feedback_id": "9e329293e022d6cdaafdec49b5f4fedc",
        "tags": expected_tags,
        "batch_id": None,
        "feedback_id_inputs": {"A": 101},
        "feedback": {"A": 201},
    }

    if as_batch:
        mock_upload_data_as_batch.assert_called_once_with(
            "foobar",
            tags["env"] if tags else "test",
            version,
            [event_1, event_2] if not (sort and timestamps is not None) else [event_2, event_1],
            BatchType.RECORD,
        )
    else:
        assert log_store.logs == [
            {
                "events": [event_1, event_2]
                if not (sort and timestamps is not None)
                else [event_2, event_1],
                "application": "foobar",
            },
        ]
        mock_upload_data_as_batch.assert_not_called()


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize("tags", [{"env": "overwrite_env"}, {}, None])
@pytest.mark.parametrize(
    "timestamps",
    [
        None,
        pd.DatetimeIndex([ANOTHER_TIME, SOME_TIME]),
        [ANOTHER_TIME, SOME_TIME],
        np.array([ANOTHER_TIME, SOME_TIME]),
    ],
)
@pytest.mark.parametrize("sort", [False, True])
@pytest.mark.parametrize("version", ["0", 0, None])
@mock.patch("gantry.logger.event_builder.uuid.uuid4")
@mock.patch("gantry.logger.client.Gantry._handle_upload")
def test__upload_data_as_batch(
    mock_handle_upload,
    mock_uuid,
    version,
    sort,
    timestamps,
    tags,
    cli_obj,
):
    mock_uuid.side_effect = ["1"]
    expected_tags = tags if tags else {"env": "test"}
    event_1 = {
        "event_id": "ABCD2" if not (sort and timestamps is not None) else "ABCD4",
        "log_timestamp": CURRENT_TIME_STR,
        "timestamp": ANOTHER_TIME_STR if timestamps is not None else CURRENT_TIME_STR,
        "metadata": {
            "environment": tags["env"] if tags else "test",
            "func_name": "foobar",
            "version": version,
            "feedback_keys": ["A"],
            "ignore_inputs": None,
            "provided_feedback_id": None,
            "feedback_version": version,
        },
        "inputs": {"A": 100},
        "outputs": {"B": 300},
        "feedback_id": "5dd14615efeb2d086e519ed35efd3f73",
        "tags": expected_tags,
        "batch_id": None,
        "feedback_id_inputs": {"A": 100},
        "feedback": {"A": 200},
    }
    event_2 = {
        "event_id": "ABCD4" if not (sort and timestamps is not None) else "ABCD2",
        "log_timestamp": CURRENT_TIME_STR,
        "timestamp": SOME_TIME_STR if timestamps is not None else CURRENT_TIME_STR,
        "metadata": {
            "environment": tags["env"] if tags else "test",
            "func_name": "foobar",
            "version": version,
            "feedback_keys": ["A"],
            "ignore_inputs": None,
            "provided_feedback_id": None,
            "feedback_version": version,
        },
        "inputs": {"A": 101},
        "outputs": {"B": 301},
        "feedback_id": "9e329293e022d6cdaafdec49b5f4fedc",
        "tags": expected_tags,
        "batch_id": None,
        "feedback_id_inputs": {"A": 101},
        "feedback": {"A": 201},
    }
    events = [event_1, event_2]

    cli_obj._upload_data_as_batch(
        "test_app", tags["env"] if tags else "test", version, events, BatchType.RECORD
    )

    mock_handle_upload.assert_called_once_with(
        mock.ANY,
        DataLink(
            application="test_app",
            version=str(version) if version is not None else version,
            file_type=UploadFileType.EVENTS,
            batch_type=BatchType.RECORD,
            log_timestamp=CURRENT_TIME.isoformat(),
            num_events=2,
            tags={"env": DataLinkElement(val=tags["env"] if tags else "test")},
        ),
        mock.ANY,
        "test_app_1",
    )


@mock.patch("gantry.logger.client.Gantry._log_predictions_and_feedbacks")
def test_log_records_preds_and_feedback_series_coerced(
    mock_preds_and_feedback,
    cli_obj,
):
    expected_inputs = pd.Series([200, 201])
    expected_outputs = pd.Series([300, 301])
    expected_feedbacks = pd.Series([100, 101])
    application = "test_app"

    cli_obj.log_records(
        application=application,
        inputs=expected_inputs,
        outputs=expected_outputs,
        feedbacks=expected_feedbacks,
    )

    downstream_kwargs = mock_preds_and_feedback.call_args.kwargs
    actual_inputs = downstream_kwargs["inputs"]
    actual_outputs = downstream_kwargs["outputs"]
    actual_feedbacks = downstream_kwargs["feedbacks"]
    pd.testing.assert_frame_equal(actual_inputs, expected_inputs.to_frame())
    pd.testing.assert_frame_equal(actual_outputs, expected_outputs.to_frame())
    pd.testing.assert_frame_equal(actual_feedbacks, expected_feedbacks.to_frame())


@pytest.mark.parametrize(
    "test_feedbacks",
    [
        [{"A": 200}, {"A": 201}],
        pd.DataFrame.from_dict({"A": [200, 201]}),
        pd.Series(name="A", data=[200, 201]),
        np.array([{"A": 200}, {"A": 201}]),
    ],
)
@pytest.mark.parametrize(
    "test_outputs",
    [
        [{"B": 300}, {"B": 301}],
        pd.DataFrame.from_dict({"B": [300, 301]}),
        pd.Series(name="B", data=[300, 301]),
        np.array([{"B": 300}, {"B": 301}]),
    ],
)
@pytest.mark.parametrize(
    "test_inputs",
    [
        [{"A": 100}, {"A": 101}],
        pd.DataFrame.from_dict({"A": [100, 101]}),
        pd.Series(name="A", data=[100, 101]),
        np.array([{"A": 100}, {"A": 101}]),
    ],
)
@pytest.mark.parametrize("version", [None, 10, "1.2.3"])
@mock.patch("gantry.logger.client.Gantry._log_predictions_and_feedbacks")
@mock.patch("gantry.logger.client.Gantry.log_predictions")
@mock.patch("gantry.logger.client.Gantry.log_feedback")
def test_log_records_preds_and_feedback(
    mock_feedback,
    mock_preds,
    mock_preds_and_feedback,
    version,
    test_inputs,
    test_outputs,
    test_feedbacks,
    cli_obj,
):
    rv = cli_obj.log_records(
        application="foobar",
        version=version,
        inputs=test_inputs,
        outputs=test_outputs,
        feedback_keys=["A"],
        feedbacks=test_feedbacks,
        timestamps=None,
        sort_on_timestamp=True,
    )
    assert rv is None

    mock_preds_and_feedback.assert_called_once()
    mock_preds.assert_not_called()
    mock_feedback.assert_not_called()


@pytest.mark.parametrize(
    "test_feedbacks",
    [
        [{"A": 200}, {"A": 201}],
        pd.DataFrame.from_dict({"A": [200, 201]}),
        pd.Series(name="A", data=[200, 201]),
        np.array([{"A": 200}, {"A": 201}]),
    ],
)
@pytest.mark.parametrize(
    "test_outputs",
    [
        [{"B": 300}, {"B": 301}],
        pd.DataFrame.from_dict({"B": [300, 301]}),
        pd.Series(name="B", data=[300, 301]),
        np.array([{"B": 300}, {"B": 301}]),
    ],
)
@pytest.mark.parametrize(
    "test_inputs",
    [
        [{"A": 100}, {"A": 101}],
        pd.DataFrame.from_dict({"A": [100, 101]}),
        pd.Series(name="A", data=[100, 101]),
        np.array([{"A": 100}, {"A": 101}]),
    ],
)
@pytest.mark.parametrize("version", [None, 10, "1.2.3"])
def test_log_records_preds_and_feedback_0_5(version, test_inputs, test_outputs, test_feedbacks):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.4):
        gantry.log_records(
            application="foobar",
            version=version,
            inputs=test_inputs,
            outputs=test_outputs,
            feedback_keys=["A"],
            feedbacks=test_feedbacks,
            timestamps=None,
            sort_on_timestamp=True,
            sample_rate=0.5,
            as_batch=False,
        )

    log_store.log_batch.assert_called_once()


@pytest.mark.parametrize(
    "test_feedbacks",
    [
        [{"A": 200}, {"A": 201}],
        pd.DataFrame.from_dict({"A": [200, 201]}),
        pd.Series(name="A", data=[200, 201]),
        np.array([{"A": 200}, {"A": 201}]),
    ],
)
@pytest.mark.parametrize(
    "test_outputs",
    [
        [{"B": 300}, {"B": 301}],
        pd.DataFrame.from_dict({"B": [300, 301]}),
        pd.Series(name="B", data=[300, 301]),
        np.array([{"B": 300}, {"B": 301}]),
    ],
)
@pytest.mark.parametrize(
    "test_inputs",
    [
        [{"A": 100}, {"A": 101}],
        pd.DataFrame.from_dict({"A": [100, 101]}),
        pd.Series(name="A", data=[100, 101]),
        np.array([{"A": 100}, {"A": 101}]),
    ],
)
@pytest.mark.parametrize("version", [None, 10, "1.2.3"])
def test_log_records_preds_and_feedback_0_5_none(
    version, test_inputs, test_outputs, test_feedbacks
):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        gantry.log_records(
            application="foobar",
            version=version,
            inputs=test_inputs,
            outputs=test_outputs,
            feedback_keys=["A"],
            feedbacks=test_feedbacks,
            timestamps=None,
            sort_on_timestamp=True,
            sample_rate=0.5,
            as_batch=False,
        )

    log_store.log_batch.assert_not_called()


@pytest.mark.parametrize(
    "test_feedbacks",
    [
        [{"A": 200}, {"A": 201}],
        pd.DataFrame.from_dict({"A": [200, 201]}),
        pd.Series(name="A", data=[200, 201]),
        np.array([{"A": 200}, {"A": 201}]),
    ],
)
@pytest.mark.parametrize(
    "test_outputs",
    [
        [{"B": 300}, {"B": 301}],
        pd.DataFrame.from_dict({"B": [300, 301]}),
        pd.Series(name="B", data=[300, 301]),
        np.array([{"B": 300}, {"B": 301}]),
    ],
)
@pytest.mark.parametrize(
    "test_inputs",
    [
        [{"A": 100}, {"A": 101}],
        pd.DataFrame.from_dict({"A": [100, 101]}),
        pd.Series(name="A", data=[100, 101]),
        np.array([{"A": 100}, {"A": 101}]),
    ],
)
@pytest.mark.parametrize("version", [None, 10, "1.2.3"])
def test_log_records_preds_and_feedback_0_0(version, test_inputs, test_outputs, test_feedbacks):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    with mock.patch("random.random", return_value=0.6):
        gantry.log_records(
            application="foobar",
            version=version,
            inputs=test_inputs,
            outputs=test_outputs,
            feedback_keys=["A"],
            feedbacks=test_feedbacks,
            timestamps=None,
            sort_on_timestamp=True,
            sample_rate=0.0,
            as_batch=False,
        )

    log_store.log_batch.assert_not_called()


@pytest.mark.parametrize(
    "test_outputs",
    [
        [{"B": 300}, {"B": 301}],
        pd.DataFrame.from_dict({"B": [300, 301]}),
        pd.Series(name="B", data=[300, 301]),
        np.array([{"B": 300}, {"B": 301}]),
    ],
)
@pytest.mark.parametrize(
    "test_inputs",
    [
        [{"A": 100}, {"A": 101}],
        pd.DataFrame.from_dict({"A": [100, 101]}),
        pd.Series(name="A", data=[100, 101]),
        np.array([{"A": 100}, {"A": 101}]),
    ],
)
@pytest.mark.parametrize("version", [None, 10, "1.2.3"])
@mock.patch("gantry.logger.client.Gantry._log_predictions_and_feedbacks")
@mock.patch("gantry.logger.client.Gantry.log_predictions")
@mock.patch("gantry.logger.client.Gantry.log_feedback")
def test_log_records_preds_only(
    mock_feedback, mock_preds, mock_preds_and_feedback, version, test_inputs, test_outputs, cli_obj
):
    rv = cli_obj.log_records(
        application="foobar",
        version=version,
        inputs=test_inputs,
        outputs=test_outputs,
        feedback_keys=["A"],
        feedbacks=None,
        timestamps=None,
        sort_on_timestamp=True,
    )
    assert rv is None

    mock_preds_and_feedback.assert_not_called()
    mock_preds.assert_called_once()
    mock_feedback.assert_not_called()


@pytest.mark.parametrize(
    "test_feedbacks",
    [
        [{"A": 200}, {"A": 201}],
        pd.DataFrame.from_dict({"A": [200, 201]}),
        pd.Series(name="A", data=[200, 201]),
        np.array([{"A": 200}, {"A": 201}]),
    ],
)
@pytest.mark.parametrize("version", [None, 10, "1.2.3"])
@mock.patch("gantry.logger.client.Gantry._log_predictions_and_feedbacks")
@mock.patch("gantry.logger.client.Gantry.log_predictions")
@mock.patch("gantry.logger.client.Gantry.log_feedback")
def test_log_records_feedback_only(
    mock_feedback, mock_preds, mock_preds_and_feedback, version, test_feedbacks, cli_obj
):
    rv = cli_obj.log_records(
        application="foobar",
        version=version,
        inputs=None,
        outputs=None,
        feedback_keys=["A"],
        feedbacks=test_feedbacks,
        timestamps=None,
        sort_on_timestamp=True,
    )
    assert rv is None

    mock_preds_and_feedback.assert_not_called()
    mock_preds.assert_not_called()
    mock_feedback.assert_called_once()


@pytest.mark.parametrize(
    "test_feedbacks",
    [None, pd.DataFrame(), [], pd.Series(), np.array([])],
)
@pytest.mark.parametrize(
    "test_outputs",
    [None, pd.DataFrame(), [], pd.Series(), np.array([])],
)
@pytest.mark.parametrize(
    "test_inputs",
    [None, pd.DataFrame(), [], pd.Series(), np.array([])],
)
@pytest.mark.parametrize("version", [None, 10, "1.2.3"])
@mock.patch("gantry.logger.client.Gantry._log_predictions_and_feedbacks")
@mock.patch("gantry.logger.client.Gantry.log_predictions")
@mock.patch("gantry.logger.client.Gantry.log_feedback")
def test_log_records_no_data(
    mock_feedback,
    mock_preds,
    mock_preds_and_feedback,
    version,
    test_inputs,
    test_outputs,
    test_feedbacks,
    cli_obj,
):
    rv = cli_obj.log_records(
        application="foobar",
        version=version,
        inputs=test_inputs,
        outputs=test_outputs,
        feedback_keys=["A"],
        feedbacks=test_feedbacks,
        timestamps=None,
        sort_on_timestamp=True,
    )
    assert rv is None

    mock_preds_and_feedback.assert_not_called()
    mock_preds.assert_not_called()
    mock_feedback.assert_not_called()


@pytest.mark.parametrize(
    "test_feedbacks",
    [None, pd.DataFrame(), [{"A": 3}, {"A": 3}], pd.Series(), np.array([])],
)
@mock.patch("gantry.logger.client.Gantry._log_predictions_and_feedbacks")
@mock.patch("gantry.logger.client.Gantry.log_predictions")
@mock.patch("gantry.logger.client.Gantry.log_feedback")
def test_log_records_incomplete_preds(
    mock_feedback,
    mock_preds,
    mock_preds_and_feedback,
    test_feedbacks,
    cli_obj,
):
    rv = cli_obj.log_records(
        application="foobar",
        version="2.0.1",
        inputs=[],
        outputs=[{"A": 1}, {"A": 2}],
        feedback_keys=["A"],
        feedbacks=test_feedbacks,
        timestamps=None,
        sort_on_timestamp=True,
    )
    assert rv is None

    mock_preds_and_feedback.assert_not_called()
    mock_preds.assert_not_called()
    mock_feedback.assert_not_called()


@mock.patch("gantry.logger.client.Gantry._log_prediction_and_feedback_event")
@mock.patch("gantry.logger.client.Gantry.log_prediction_event")
@mock.patch("gantry.logger.client.Gantry.log_feedback_event")
def test_log_record_pred_and_feedback(mock_feedback, mock_pred, mock_pred_and_feedback, cli_obj):
    cli_obj.log_record(
        application="foobar",
        version="2.0.1",
        inputs={"A": 100},
        outputs={"B": 300},
        feedback_keys=["A"],
        feedback={"A": 200},
        timestamp=None,
    )

    mock_pred_and_feedback.assert_called_once_with(
        application="foobar",
        version="2.0.1",
        inputs={"A": 100},
        outputs={"B": 300},
        feedback={"A": 200},
        feedback_keys=["A"],
        ignore_inputs=None,
        timestamp=None,
        sample_rate=1.0,
        tags=None,
    )
    mock_pred.assert_not_called()
    mock_feedback.assert_not_called()


@pytest.mark.parametrize(
    "test_feedback",
    [None, {}],
)
@mock.patch("gantry.logger.client.Gantry._log_prediction_and_feedback_event")
@mock.patch("gantry.logger.client.Gantry.log_prediction_event")
@mock.patch("gantry.logger.client.Gantry.log_feedback_event")
def test_log_record_pred_only(
    mock_feedback, mock_pred, mock_pred_and_feedback, test_feedback, cli_obj
):
    cli_obj.log_record(
        application="foobar",
        version="2.0.1",
        inputs={"A": 100},
        outputs={"B": 300},
        feedback_keys=["A"],
        feedback=test_feedback,
        timestamp=None,
    )

    mock_pred_and_feedback.assert_not_called()
    mock_pred.assert_called_once_with(
        application="foobar",
        inputs={"A": 100},
        outputs={"B": 300},
        version="2.0.1",
        feedback_keys=["A"],
        ignore_inputs=None,
        feedback_id=None,
        timestamp=None,
        sample_rate=1.0,
        tags=None,
    )
    mock_feedback.assert_not_called()


@pytest.mark.parametrize(
    "test_output",
    [None, {}],
)
@pytest.mark.parametrize(
    "test_input",
    [None, {}],
)
@mock.patch("gantry.logger.client.Gantry._log_prediction_and_feedback_event")
@mock.patch("gantry.logger.client.Gantry.log_prediction_event")
@mock.patch("gantry.logger.client.Gantry.log_feedback_event")
def test_log_record_feedback_only(
    mock_feedback, mock_pred, mock_pred_and_feedback, test_input, test_output, cli_obj
):
    cli_obj.log_record(
        application="foobar",
        version="2.0.1",
        inputs=test_input,
        outputs=test_output,
        feedback_keys=["A"],
        feedback={"A": 200},
        timestamp=None,
    )

    mock_pred_and_feedback.assert_not_called()
    mock_pred.assert_not_called()
    mock_feedback.assert_called_once_with(
        application="foobar",
        feedback_id=None,
        feedback={"A": 200},
        feedback_version="2.0.1",
        timestamp=None,
        sample_rate=1.0,
        tags=None,
    )


@pytest.mark.parametrize(
    "test_input",
    [None, {}],
)
@mock.patch("gantry.logger.client.Gantry._log_prediction_and_feedback_event")
@mock.patch("gantry.logger.client.Gantry.log_prediction_event")
@mock.patch("gantry.logger.client.Gantry.log_feedback_event")
def test_log_record_no_data(mock_feedback, mock_pred, mock_pred_and_feedback, test_input, cli_obj):
    cli_obj.log_record(
        application="foobar",
        version="2.0.1",
        inputs=test_input,
        outputs={"B": 100},
        feedback_keys=["A"],
        feedback=None,
        timestamp=None,
    )

    mock_pred_and_feedback.assert_not_called()
    mock_pred.assert_not_called()
    mock_feedback.assert_not_called()


@pytest.mark.parametrize("feedback", [None, {}, {"B": 200}])
@mock.patch("gantry.logger.client.Gantry._log_prediction_and_feedback_event")
@mock.patch("gantry.logger.client.Gantry.log_prediction_event")
@mock.patch("gantry.logger.client.Gantry.log_feedback_event")
def test_log_record_incomplete_preds(
    mock_feedback, mock_pred, mock_pred_and_feedback, feedback, cli_obj
):
    cli_obj.log_record(
        application="foobar",
        version="2.0.1",
        inputs={},
        outputs={"B": 100},
        feedback_keys=["A"],
        feedback=feedback,
        timestamp=None,
    )

    mock_pred_and_feedback.assert_not_called()
    mock_pred.assert_not_called()
    mock_feedback.assert_not_called()


@pytest.mark.parametrize(
    "test_inputs",
    [[{"A": 100}, {"A": 101}]],
)
@mock.patch("gantry.logger.utils.get_file_linecount")
def test_log_file(mock_line_count, test_inputs):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")
    mock_line_count.return_value = 5

    gantry.log_file(
        "foobar",
        "dir/csv_with_headers.csv",
        version="2.0.1",
    )

    log_store.log_batch.assert_not_called()


@pytest.mark.parametrize(
    "tags, expected_env",
    [
        [None, "test"],
        [{}, "test"],
        [{"other_tag": "random"}, "test"],
        [{"env": "overwrite_env"}, "overwrite_env"],
    ],
)
def test_get_env_and_context(tags, expected_env):
    log_store = mock.MagicMock()
    gantry = client.Gantry(log_store=log_store, environment="test")

    environment, context = gantry._get_env_and_context(tags)

    assert environment == expected_env
    assert context == {"environment": expected_env}
