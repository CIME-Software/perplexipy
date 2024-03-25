# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from perplexipy import PerplexityClient
from perplexipy import __VERSION__

import os
import select
import sys

import click


# *** implementation ***

def _die(msg: str, exitCode: int = 99):
    click.echo(msg)
    sys.exit(99)


def _helpUser() -> str:
    return "Syntax: codex 'your coding question here in single quotes'\n"


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
    result = None
    if userQuery:
        client = PerplexityClient(key = os.environ['PERPLEXITY_API_KEY'])
        client.model = 'codellama-70b-instruct'
        result = client.query(userQuery)

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
        userQuery = 'Concise, code only answer to this question: '+' '.join(tokens)
    elif _stdinHasData():
        userQuery = _assembleInput()
        userQuery = 'Give me a concise coding example to answer this question: '+userQuery

    if userQuery:
        result = codexCore(userQuery)
        click.echo(result)
    else:
        _die(_helpUser(), 1)

    return result


if '__main__' == __name__:
    codex()

