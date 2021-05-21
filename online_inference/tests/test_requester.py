import os
from unittest.mock import patch
from argparse import Namespace
from urllib import parse

import pytest

from requester import main

TEST_DATA = os.path.join("test_data", "test.csv")
TARGET_COL = "target"


@pytest.fixture
def post_test(test_client):
    def mocked_post(url, **kwargs):
        url_info = parse.urlparse(url)
        return test_client.post(url_info.path, json=kwargs["json"])
    return mocked_post


@ patch("requester.requests.post")
def test_prediction(mock_request_post, post_test, capsys):
    num_examples = 5
    params = Namespace(host="localhost", port=2000, num_examples=num_examples,
                       test_csv=TEST_DATA, target=TARGET_COL, url="/predict")
    mock_request_post.side_effect = post_test
    main(params)

    captured = capsys.readouterr()
    assert len(captured.out.splitlines()) == num_examples
    assert "Actual label" in captured.out and "Predicted label" in captured.out
