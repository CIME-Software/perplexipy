# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from appdirs import AppDirs
from prompt_toolkit import HTML
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as printF
from prompt_toolkit.enums import EditingMode

from perplexipy import PerplexityClient
from perplexipy import __VERSION__

import os
import select
import sys

import click
import yaml


# *** constants ***

ARG_REPL = 'repl'
"""
@private
"""

CONFIG_PATH = AppDirs(appname = 'PerplexiPy').user_config_dir
"""
@private
"""
CONFIG_FILE_NAME = os.path.join(CONFIG_PATH, 'codex-repl.yaml')
"""
@private
"""

DEFAULT_LLM = 'mixtral-8x7b-instruct'
DEFAULT_VIM_EDIT_MODE = True
"""
@private
"""

QUERY_CRISP = 'Concise, code only reply to this prompt: '
"""
@private
"""

QUERY_DETAILED = 'Give me a concise coding example and include URL references in reply this prompt: '
"""
@private
"""


# *** globals ***

_client = PerplexityClient(key = os.environ['PERPLEXITY_API_KEY'])
_client.model = DEFAULT_LLM
_queryCodeStyle = True


# *** implementation ***

def _die(msg: str, exitCode: int = 99):
    click.echo(msg)
    sys.exit(99)


def _helpUser() -> str:
    return "Syntax: codex repl | 'your coding question here in single quotes'\n"


def codexCore(userQuery: str) -> str:
    """
    Send a user query to the model for processing.

    Arguments
    ---------
        userQuery
    A string with the user query, most often a programming question.

    Returns
    -------
    The result of the query, or `None` if the query was empty.
    """
    global _client

    result = None
    if userQuery:
        if not _client:
            _client = PerplexityClient(key = os.environ['PERPLEXITY_API_KEY'])
            _client.model = DEFAULT_LLM
        result = _client.query(userQuery)

    return result


def _stdinHasData() -> bool:
    """
    Checks if there's data pending to be processed off `stdin`.  It's a
    convinience function for readability.

    Returns
    -------
    `True` if the `stdin` stream is pending processing.
    """
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def _assembleInput() -> str:
    result = ''
    for line in sys.stdin:
        result += line

    return result


def _activeModel(modelID: int = 0) -> str:
    if modelID:
        try:
            ref = modelID-1
            model = list(_client.models.keys())[ref]
            _client.model = model
        except:
            click.secho('Invalid model ID = %s' % modelID, bg = 'red', fg = 'white')
    click.secho('Active model: %s\n' % _client.model, fg = 'green', bold = True)
    return modelID


def _REPLHello():
    click.clear()
    printF(HTML('PerplexiPy <b><ansigreen>Codex playground - coding, scripting, and sysops assistant</ansigreen></b>'))
    _activeModel()
    printF(HTML('Enter <b>/help</b> for commands list'))
    print()


def _helpREPL():
    print("""
/active [modelID] - display active model or set active to modelID
/cinfo - display configuration info
/clear - clear the screen
/exit - end Codex and return to the command prompt
/help - this commands list help
/mode [mode] - display or set the editing mode to vi or emacs
/models - list available models; n = modelID
/quit - alias for /exit
/style [style] - display or set query style to code or human
/version - display the Codex + PerplexiPy version
? - alias for /help
""")


def _displayModels() -> str:
    _activeModel()
    print('Available models:\n')
    n = 1
    for model in _client.models.keys():
        print('%2d - %s' % (n, model))
        n += 1
    print()


def _editingMode(session: PromptSession, mode = None):
    if mode:
        mode = mode.lower()
        newEditingMode = EditingMode.EMACS if mode == 'emacs' else EditingMode.VI
        session = PromptSession(editing_mode = newEditingMode)

    editingMode = str(session.editing_mode).replace('EditingMode.', '').lower()
    click.secho('Editing mode = %s' % editingMode, fg = 'bright_blue')

    return session


def _queryStyle(newStyle: str = None):
    global _queryCodeStyle

    if newStyle:
        _queryCodeStyle = newStyle != 'human'
    click.secho('Coding query style = %s' % _queryCodeStyle, fg = 'bright_blue')
    return _queryCodeStyle


def _makeQuery(userQuery: str) -> str:
    if _queryCodeStyle:
        userQuery = QUERY_DETAILED+userQuery

    return codexCore(userQuery)


def _displayVersion():
    click.secho('PerplexiPy Codex version %s\n' % __VERSION__, fg = 'bright_green')


def _saveConfigTo(config: dict, fileName: str = CONFIG_FILE_NAME, pathName = CONFIG_PATH):
    if not os.path.exists(pathName):
        os.makedirs(pathName)
    with open(fileName, 'w') as outputFile:
        yaml.dump(config, outputFile)


def _loadConfigFrom(fileName: str = CONFIG_FILE_NAME, pathName = CONFIG_PATH) -> dict:
    if os.path.exists(fileName):
        with open(fileName, 'r') as inputFile:
            config = yaml.safe_load(inputFile)
    else:
        config = {
            'activeModel': 3,
            'editingMode': 'vi',
            'queryCodeStyle': _queryCodeStyle,
        }
        _saveConfigTo(config, fileName, pathName)
    return config


def _displayConfigInfo():
    pass
    click.secho('Config file: %s' % CONFIG_FILE_NAME)
    click.secho(str(_loadConfigFrom())+'\n')


# TODO: Refactor REPL - https://github.com/CIME-Software/perplexipy/issues/46
def _runREPL() -> str:
    """
    Run a REPL loop for sending queries to the AI provider.

    Returns
    -------
    The word "REPL" to signal to the `codex` command that it received valid
    input.
    """
    _REPLHello()
    config = _loadConfigFrom()
    session = PromptSession()
    _activeModel(config['activeModel'])
    session = _editingMode(session, config['editingMode'])
    _queryStyle('code' if config['queryCodeStyle'] else 'human')
    while True:
        userQuery = session.prompt('Ask anything (/exit to end): ')
        if userQuery[0] in ('/', '?', ':'):
            parts = userQuery.split(' ')
            command = parts[0]
            if command in ('/exit', '/quit', ':q', '/q'):
                sys.exit(0)
            elif command == '/active':
                if len(parts) > 1:
                    try:
                        model = int(parts[1])
                        config['activeModel'] = _activeModel(model)
                        _saveConfigTo(config)
                    except:
                        _activeModel()
                else:
                    _activeModel()
            elif command == '/cinfo':
                _displayConfigInfo()
            elif command == '/clear':
                click.clear()
                _editingMode(session)
            elif command in ('/help', '?'):
                _helpREPL()
            elif command == '/mode':
                if len(parts) > 1:
                    try:
                        session = _editingMode(session, parts[1])
                        config['editingMode'] = parts[1]
                        _saveConfigTo(config)
                    except:
                        pass
                else:
                    _editingMode(session)
            elif command == '/models':
                _displayModels()
            elif command == '/style':
                if len(parts) > 1:
                    queryStyleType = parts[1]
                    config['queryCodeStyle'] = _queryStyle(queryStyleType)
                    _saveConfigTo(config)
                else:
                    _queryStyle()
            elif command == '/version':
                _displayVersion()
            continue
        result = _makeQuery(userQuery)
        print('%s' % result)
        click.secho('--------------------------------------------------', fg = 'green')
        print()

    return 'REPL'


@click.command('codex')
@click.version_option(__VERSION__, prog_name = 'codex')
@click.argument('tokens', nargs = -1, type = click.STRING)
def codex(tokens: list) -> str:
    """
    Process a command line query and display the result to the console.

    Arguments
    ---------
        tokens
    A list of tokens that will be assembled as a single string for
    processing.

    Returns
    -------
    A string with the response to the query, after displaying it to the
    console.
    """
    result = None
    userQuery = None
    if len(tokens):
        if len(tokens) == 1 and tokens[0].lower() == ARG_REPL:
            userQuery = _runREPL()
        else:
            userQuery = QUERY_CRISP+''.join(tokens)
    elif _stdinHasData():
        userQuery = _assembleInput()
        userQuery = QUERY_DETAILED+userQuery

    if userQuery:
        result = codexCore(userQuery)
        click.echo(result)
    else:
        _die(_helpUser(), 1)

    return result


if '__main__' == __name__:
    codex()

