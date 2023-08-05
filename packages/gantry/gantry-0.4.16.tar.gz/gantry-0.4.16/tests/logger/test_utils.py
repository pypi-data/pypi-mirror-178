import json
from io import StringIO

import mock
import pandas as pd
import pytest
import responses

from gantry.exceptions import (  # noqa
    GantryBatchCreationException,
    GantryLoggingException,
)
from gantry.logger.utils import (
    _build_batch_iterator,
    _concurrent_upload_multipart_batch,
    _is_empty,
    _is_not_empty,
    _log_exception,
    _put_block,
)


@pytest.mark.parametrize(
    ["test_obj", "expected_result"],
    [
        (pd.DataFrame(), True),
        (pd.DataFrame.from_dict({"A": [200, 201]}), False),
        ([1, 2, 3], False),
        ([], True),
        (None, True),
    ],
)
def test_is_empty(test_obj, expected_result):
    assert _is_empty(test_obj) is expected_result


@pytest.mark.parametrize(
    ["test_obj", "expected_result"],
    [
        (pd.DataFrame(), False),
        (pd.DataFrame.from_dict({"A": [200, 201]}), True),
        ([1, 2, 3], True),
        ([], False),
        (None, False),
    ],
)
def test_is_not_empty(test_obj, expected_result):
    assert _is_not_empty(test_obj) is expected_result


def test_log_exception():
    try:
        _log_exception(lambda: exec("raise(GantryLoggingException())"))()
    except Exception as e:
        pytest.fail(f"_log_exception() failed due to raising {e}")
    with pytest.raises(GantryBatchCreationException):
        _log_exception(lambda: exec("raise(GantryBatchCreationException())"))()
    try:
        _log_exception(lambda: exec("raise(Exception())"))()
    except Exception as e:
        pytest.fail(f"_log_exception() failed due to raising {e}")


def test_build_batch_iterator():
    event_list = [{1: 1}, {2: 2}, {3: 3}, {4: 4}, {5: 5}]
    # We should only have 3 batches created from the list.
    batch_iter = _build_batch_iterator(event_list, 2)
    iters = 0
    for _ in batch_iter:
        iters += 1
    assert iters == 3

    # We should still have all 5 lines in the file
    batch_iter = _build_batch_iterator(event_list, 2)
    result = "".join([part.decode("utf-8") for part in batch_iter])
    file = StringIO(result)

    for line in file.readlines():
        json.loads(line)

    file.seek(0)
    assert len(file.readlines()) == 5


def test_put_block():
    with responses.RequestsMock() as resp:
        resp.add(
            resp.PUT,
            url="http://foo/bar",
            headers={"ETag": "0123456789", "Content-Type": "application/json"},
        )
        res = _put_block("http://foo/bar", 10, {"foo": "bar"})
        assert res == {"ETag": "0123456789", "PartNumber": 10}


@mock.patch("gantry.logger.utils._put_block")
def test_concurrent_upload(mock_put_block):
    mock_put_block.side_effect = [
        {"ETag": "123", "PartNumber": 2},
        {"ETag": "456", "PartNumber": 1},
        {"ETag": "789", "PartNumber": 3},
    ]

    data = [{"1": "foo"}, {"2": "bar"}, {"3": "baz"}]
    signed_urls = ["http://foo", "http://bar", "http://baz"]

    ret = _concurrent_upload_multipart_batch(iter(data), signed_urls)
    assert ret == [
        {"ETag": "456", "PartNumber": 1},
        {"ETag": "123", "PartNumber": 2},
        {"ETag": "789", "PartNumber": 3},
    ]
