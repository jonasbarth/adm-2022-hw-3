"""Unit tests for HTML reader."""
import os

import pytest

from util import read_html_from


@pytest.fixture
def path():
    return './test_html.html'


@pytest.fixture(autouse=True)
def assert_no_file(path):
    assert not os.path.exists(path)
    with open(path, 'w') as file:
        file.write('testing')
    yield
    os.remove(path)
    assert not os.path.exists(path)


def test_that_html_file_read(path):
    html = read_html_from(path)

    assert html == 'testing'
