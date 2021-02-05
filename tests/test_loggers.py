import pytest

from ct8_refresh.loggers import Loggers


@pytest.fixture
def loggers():
    return Loggers()


def test_add_file_logger(loggers):
    assert loggers.file_handler_id
    assert Loggers(debug_switch=True).file_handler_id


def test_add_stderr(loggers):
    assert loggers.stderr_handler_id
