# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


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


# *** constants ***

ARG_REPL = 'repl'
DEFAULT_VIM_EDIT_MODE=True
QUERY_CRISP = 'Concise, code only reply to this prompt: '
QUERY_DETAILED = 'Give me a concise coding example and include URL references in reply this prompt: '


# *** globals ***

_client = PerplexityClient(key = os.environ['PERPLEXITY_API_KEY'])
_client.model = 'codellama-70b-instruct'


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
            _client.model = 'codellama-70b-instruct'
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


def _REPLHello():
    printF(HTML('PerplexiPy <b><ansigreen>codex - coding, scripting, and sysops assistant</ansigreen></b>'))
    _activeModel()
    printF(HTML('Enter <b>/help</b> for commands list'))
    print()


def _helpREPL():
    print("""
/active [modelID] - display active model or set active to modelID
/clear - clear the screen
/exit - end codex and return to the command prompt
/help - this commands list help
/mode [mode] - display or set the editing mode to vi or emacs
/models - list available models; n = modelID
/quit - alias for /exit
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


def _runREPL() -> str:
    """
    Run a REPL loop for sending queries to the AI provider.

    Returns
    -------
    The word "REPL" to signal to the `codex` command that it received valid
    input.
    """
    _REPLHello()
    session = PromptSession(vi_mode = True)
    _editingMode(session)
    while True:
        userQuery = session.prompt('Ask anything (/exit to end): ')
        if userQuery[0] in ('/', '?', ':'):
            parts = userQuery.split(' ')
            command = parts[0]
            if command in ('/exit', '/quit', ':q'):
                sys.exit(0)
            elif command == '/active':
                if len(parts) > 1:
                    try:
                        _activeModel(int(parts[1]))
                    except:
                        _activeModel()
                else:
                    _activeModel()
            elif command == '/clear':
                click.clear()
                _editingMode(session)
            elif command in ('/help', '?'):
                _helpREPL()
            elif command == '/mode':
                if len(parts) > 1:
                    try:
                        session = _editingMode(session, parts[1])
                    except:
                        pass
                else:
                    _editingMode(session)
            elif command == '/models':
                    _displayModels()
            continue
        result = codexCore(QUERY_DETAILED+userQuery)
        print('%s' % result)
        print('--------------------------------------------------')
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

