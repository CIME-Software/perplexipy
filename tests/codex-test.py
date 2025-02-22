# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from unittest.mock import patch

from click.testing import CliRunner
from perplexipy.codex import CodexREPL
from perplexipy.codex import DEFAULT_MODEL_NAME
from perplexipy.codex import _die # noqa: F401
from perplexipy.codex import codex
from perplexipy.codex import codexCore
from prompt_toolkit import PromptSession
from prompt_toolkit.enums import EditingMode

import os
import pytest
import tempfile


TEST_QUERY = 'How do I declare a variable in Dart?'
TEST_CONFIG_PATH = tempfile.TemporaryDirectory().name
TEST_CONFIG_FILE_NAME = os.path.join(TEST_CONFIG_PATH, 'codex-repl.yaml')


# *** globals ***

_codex = None # test_CodexREPL() initializes it


# *** fixtures ***

@pytest.fixture
def configFileName():
    return TEST_CONFIG_FILE_NAME


@pytest.fixture
def configPath():
    return TEST_CONFIG_PATH


@pytest.fixture(autouse = True)
def stdoutHide(monkeypatch):
    monkeypatch.setattr('sys.stdout', open('/dev/null', 'w'))


@pytest.fixture
def codexInstance():
    if not _codex:
        raise RuntimeError("test_CodexREPL() hasn't been executed!")

    return _codex


# *** tests ***

@pytest.mark.skip("_die() doesn't require a unit test")
def test__die():
    pass


def test_CodexREPL():
    global _codex

    _codex = CodexREPL()


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


def test_CodexRepl__loadConfigFrom(codexInstance, configFileName, configPath):
    print(configPath)
    bogusPath = tempfile.TemporaryDirectory().name
    bogusFileName = os.path.join(bogusPath, 'codex-repl.yaml')
    assert not os.path.exists(bogusPath)
    assert not os.path.exists(bogusFileName)
    config = codexInstance._loadConfigFrom(configFileName, configPath)
    assert os.path.exists(configPath)
    assert os.path.exists(configFileName)
    assert isinstance(config, dict)
    assert config['activeModel'] == DEFAULT_MODEL_NAME
    assert config['activeModel'] in codexInstance.displayModels()

    # Config file already exists:
    config = codexInstance._loadConfigFrom(configFileName, configPath)
    assert isinstance(config, dict)


def test_CodexREPL_displayModels(codexInstance):
    models = codexInstance.displayModels()
    assert models
    assert isinstance(models, list)
    assert DEFAULT_MODEL_NAME in models


def test_CodexREPL_activateModel(codexInstance):
    model = codexInstance.activeModel()
    assert model
    assert isinstance(model, str)

    models = codexInstance.displayModels()

    modelID = len(models)
    model = codexInstance.activeModel(modelID)
    assert models[modelID-1] == model
    modelID = 2
    model = codexInstance.activeModel(modelID)
    assert models[modelID-1] == model


def test_CodexREPL_editingMode(codexInstance):
    session = PromptSession()
    editingMode = codexInstance._editingMode
    session = codexInstance.editingMode(session, str(EditingMode.EMACS).replace('EditingMode.', ''))
    assert codexInstance._editingMode == EditingMode.EMACS
    session = codexInstance.editingMode(session, str(editingMode).replace('EditingMode.', ''))
    assert codexInstance._editingMode == editingMode


def test_CodexREPL_queryStyle(codexInstance):
    queryStyle = codexInstance.queryCodeStyle
    newStyle = 'human' if queryStyle else 'code'
    codexInstance.queryCodeStyle = newStyle
    assert ('human' if not codexInstance.queryCodeStyle else 'code') == newStyle
    codexInstance.queryCodeStyle = 'bogus'
    assert codexInstance.queryCodeStyle
    codexInstance.queryCodeStyle = queryStyle


def test_CodexREPL_makeQuery(codexInstance):
    result = codexInstance.makeQuery(TEST_QUERY)
    assert result
    assert isinstance(result, str)

    with pytest.raises(ValueError):
        assert not codexInstance.makeQuery('')
    with pytest.raises(ValueError):
        assert not codexInstance.makeQuery(None)


test_CodexREPL()
test_CodexRepl__loadConfigFrom(_codex, TEST_CONFIG_FILE_NAME, TEST_CONFIG_PATH)
test_CodexREPL_editingMode(_codex)
test_CodexREPL_queryStyle(_codex)
test_CodexREPL_makeQuery(_codex)


