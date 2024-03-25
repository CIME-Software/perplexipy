# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from unittest import mock

from click.testing import CliRunner
from perplexipy.codex import codexCore
from perplexipy.codex import codex

import io
import sys


TEST_QUERY = 'How do I declare a variable in Dart?'


# *** tests ***

def test_codexCore():
    result = codexCore(TEST_QUERY)
    assert result
    assert isinstance(result, str)

    assert not codexCore('')
    assert not codexCore(None)


def test_codex():
    runner = CliRunner()
    result = runner.invoke(codex, [ TEST_QUERY, ])
    assert str(result) == '<Result okay>'
    result = runner.invoke(codex, [ ])
    assert str(result) != '<Result okay>'

    # stdin input
    with mock.patch('sys.stdin', io.StringIO(TEST_QUERY)):
        result = runner.invoke(codex, [ ])

    assert str(result) != '<Result okay>'

test_codex()

