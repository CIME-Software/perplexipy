# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from unittest.mock import patch

from click.testing import CliRunner
from perplexipy.codex import DEFAULT_MODEL_NAME
from perplexipy.codex import _activeModel
from perplexipy.codex import _displayModels
from perplexipy.codex import _loadConfigFrom
from perplexipy.codex import codex
from perplexipy.codex import codexCore

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


@pytest.fixture(autouse = True)
def stdoutHide(monkeypatch):
    monkeypatch.setattr('sys.stdout', open('/dev/null', 'w'))


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
    assert config['activeModel'] == DEFAULT_MODEL_NAME
    assert config['activeModel'] in _displayModels()

    # Config file already exists:
    config = _loadConfigFrom(_configFileName, _configPath)
    assert isinstance(config, dict)


def test__displayModels():
    models = _displayModels()
    assert models
    assert isinstance(models, list)
    assert DEFAULT_MODEL_NAME in models


def test__activateModel():
    model = _activeModel()
    assert model
    assert isinstance(model, str)

    models = _displayModels()

    modelID = len(models)
    model = _activeModel(modelID)
    assert models[modelID-1] == model
    modelID = 2
    model = _activeModel(modelID)
    assert models[modelID-1] == model

