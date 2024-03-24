# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from perplexipy import PerplexityClient
from perplexipy import __VERSION__

import os
import sys

import click


# *** implementation ***

def _die(msg: str, exitCode: int = 99):
    click.echo(msg)
    sys.exit(99)


def _helpUser() -> str:
    return "Syntax: codex 'your coding question here in single quotes'\n"


def codexCore(userQuery: str) -> str:
    result = None
    if userQuery:
        client = PerplexityClient(key = os.environ['PERPLEXITY_API_KEY'])
        client.model = 'codellama-70b-instruct'
        result = client.query(userQuery)

    return result


@click.command('codex')
@click.version_option(__VERSION__, prog_name = 'codex')
@click.argument('tokens', nargs = -1, type = click.STRING)
def codex(tokens):
    result = None
    if len(tokens):
        userQuery = 'Concise, code only answer to this question: '+' '.join(tokens)
        result = codexCore(userQuery)
        click.echo(result)
    else:
        _die(_helpUser(), 1)

    return result


if '__main__' == __name__:
    codex()

