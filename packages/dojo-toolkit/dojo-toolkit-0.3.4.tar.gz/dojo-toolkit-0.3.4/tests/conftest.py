try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from dojo_toolkit.code_handler import DojoCodeHandler


@pytest.fixture
def mocked_code_handler():
    code_handler = DojoCodeHandler(notifier=mock.Mock(),
                                   test_runner=mock.Mock(),
                                   sound_player=mock.Mock())
    return code_handler
