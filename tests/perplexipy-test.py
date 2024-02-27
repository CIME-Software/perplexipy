# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt

from perplexipy import PerplexityClient
from perplexipy import PerplexityClientError

import pytest


# +++ constants +++

TEST_BOGUS_MODEL = 'bogus-llm-1b'
TEST_QUERY = 'Brief answer to the ultimate question about life, the Universe, and everything?'


# +++ globals +++

_testClient = None


# +++ fixtures +++

@pytest.fixture
def testClient():
    global _testClient

    if not _testClient:
        _testClient = PerplexityClient()

    return _testClient


def test_PerplexityClient():
    with pytest.raises(PerplexityClientError):
        PerplexityClient(None)
    with pytest.raises(PerplexityClientError):
        PerplexityClient('')
    with pytest.raises(PerplexityClientError):
        PerplexityClient('xxxx')


def test_PerplexityClient_query(testClient):
    result = testClient.query(TEST_QUERY)
    assert isinstance(result, str)
    assert len(result)

    with pytest.raises(Exception):
        testClient.query((TEST_QUERY, 'xxxx'))


def test_PerplexityClient_bogusModel(testClient):
    model = testClient.model
    testClient.model = TEST_BOGUS_MODEL
    with pytest.raises(Exception):
        testClient.query(TEST_QUERY)

    testClient.model = model
    result = testClient.query(TEST_QUERY)
    assert result

# _testClient = PerplexityClient()
# test_PerplexityClient_bogusModel(_testClient)

