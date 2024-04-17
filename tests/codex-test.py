# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from unittest.mock import patch

from click.testing import CliRunner
from perplexipy.codex import codexCore
from perplexipy.codex import codex
from perplexipy.codex import _loadConfigFrom

import os
import pytest
import tempfile


TEST_QUERY = 'How do I declare a variable in Dart?'
TEST_CONFIG_PATH = tempfile.TemporaryDirectory().name
TEST_CONFIG_FILE_NAME = os.path.join(TEST_CONFIG_PATH, 'codex-repl.yaml')


# *** fixtures ***

@pytest.fixture
def _configFileName():
    return TEST_CONFIG_FILE_NAME


@pytest.fixture
def _configPath():
    return TEST_CONFIG_PATH


# *** tests ***

def test_codexCore():
    result = codexCore(TEST_QUERY)
    assert result
    assert isinstance(result, str)

    assert not codexCore('')
    assert not codexCore(None)


@patch('sys.stdin')
def test_codex(stdinMock):
    runner = CliRunner()
    result = runner.invoke(codex, [ TEST_QUERY, ])
    assert str(result) == '<Result okay>'
    result = runner.invoke(codex, [ ])
    assert str(result) != '<Result okay>'

    # stdin input
    stdinMock.read.return_value = TEST_QUERY
    result = runner.invoke(codex, [ ])


def test__loadConfigFrom(_configFileName, _configPath):
    assert not os.path.exists(_configPath)
    assert not os.path.exists(_configFileName)
    config = _loadConfigFrom(_configFileName, _configPath)
    assert os.path.exists(_configPath)
    assert os.path.exists(_configFileName)
    assert isinstance(config, dict)

    # Config file already exists:
    config = _loadConfigFrom(_configFileName, _configPath)
    assert isinstance(config, dict)


# test__loadConfigFrom(TEST_CONFIG_FILE_NAME, TEST_CONFIG_PATH)

