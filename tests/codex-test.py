# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from unittest.mock import patch

from click.testing import CliRunner
from perplexipy.codex import codexCore
from perplexipy.codex import codex


TEST_QUERY = 'How do I declare a variable in Dart?'


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

# test_codex()

