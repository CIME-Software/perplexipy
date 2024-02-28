# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt

from perplexipy import PerplexityClient
from perplexipy import PerplexityClientError
from perplexipy import Responses

import pytest


# +++ constants +++

TEST_BOGUS_MODEL = 'bogus-llm-1b'
TEST_QUERY = 'Brief answer to the ultimate question about life, the Universe, and everything?'
TEST_QUERY_LONG = 'Give me a comprehensive list of US presidents.'


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


def test_PerplexityClient_queryBatch(testClient):
    result = testClient.queryBatch(TEST_QUERY)
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)


def test_PerplexityClient_queryStreamable(testClient):
    t = ''
    results = testClient.queryStreamable(TEST_QUERY_LONG)
    assert isinstance(results, Responses)
    for result in results:
        assert isinstance(result, str)
        t += result
    assert len(t)

    with pytest.raises(PerplexityClientError):
        testClient.queryStreamable('')
    with pytest.raises(PerplexityClientError):
        testClient.queryStreamable(None)


# _testClient = PerplexityClient()
# test_PerplexityClient_queryStreamable(_testClient)

