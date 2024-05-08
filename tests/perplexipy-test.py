# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt

from perplexipy import PERPLEXITY_API_KEY
from perplexipy import PerplexityClient
from perplexipy import _CLAUDE_MODEL
from perplexipy.errors import PerplexityClientError
from perplexipy.responses import Responses

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
        _testClient = PerplexityClient(key = PERPLEXITY_API_KEY)

    return _testClient


def test_PerplexityClient():
    with pytest.raises(PerplexityClientError):
        PerplexityClient(None)
    with pytest.raises(PerplexityClientError):
        PerplexityClient('')
    with pytest.raises(PerplexityClientError):
        PerplexityClient('xxxx')
    with pytest.raises(PerplexityClientError):
        PerplexityClient(PERPLEXITY_API_KEY+'😊')


def test_PerplexityClient_query(testClient):
    result = testClient.query(TEST_QUERY)
    assert isinstance(result, str)
    assert len(result)

    with pytest.raises(Exception):
        testClient.query((TEST_QUERY, 'xxxx'))


def test_PerplexityClient_modelAccessors(testClient):
    with pytest.raises(Exception):
        testClient.model = TEST_BOGUS_MODEL

    with pytest.raises(Exception):
        testClient.model = None

    originalModel = testClient.model
    unitTestState = testClient._unitTest
    testClient._unitTest = True
    with pytest.raises(Exception):
        testClient.model = _CLAUDE_MODEL
    testClient._unitTest = unitTestState
    testClient.model = originalModel


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


def test_PerplexityClient_models(testClient):
    model = testClient.model
    models = testClient.models
    assert isinstance(models, dict)
    assert model in models.keys()


# _testClient = PerplexityClient(key = PERPLEXITY_API_KEY)
# test_PerplexityClient_modelAccessors(_testClient)
