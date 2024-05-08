# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from collections import OrderedDict

import importlib.metadata


__VERSION__ = importlib.metadata.version('PerplexiPy')


"""
.. include:: ../README.md

---

# PerplexiPy API Documentation
"""


from collections import namedtuple

from dotenv import load_dotenv
from openai import OpenAI

from perplexipy.errors import PerplexityClientError
from perplexipy.responses import Responses

load_dotenv()

import os


_CLAUDE_MODEL = 'claude-3-haiku'
PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY', default = '')
"""
`PERPLEXITY_API_KEY` is set to the environment variable of the same name if
present, otherwise it's set to the empty string `''`.  PerplexiPy uses the
`dotenv` module to load environment settings from `$PWD/.env` if present.
"""
PERPLEXITY_API_PREFIX = 'pplx-'
PERPLEXITY_API_URL = 'https://api.perplexity.ai'
PERPLEXITY_DEFAULT_MODEL = 'llama-3-sonar-small-32k-chat'
PERPLEXITY_DEFAULT_ROLE = 'user'
PERPLEXITY_TIMEOUT = 30.0 # seconds
PERPLEXITY_VALID_ROLES = { 'assistant', 'system', 'user', } # future proofing.


"""
Immutable dictionary-like object of a model's capabilities.  Use `_asDict()` if
dictionary manipulation is required.
"""
ModelInfo = namedtuple('ModelInfo', [ 'parameterCount', 'contextLength', 'modelType', 'availability', ])


class PerplexityClient:
    """
    PerplexityClient objects encapsulate all the API functionality.  They can be
    instantiated across multiple contexts, each keeping its own state.
    """
    def __init__(self, key: str, endpoint:str = PERPLEXITY_API_URL, unitTest = False):
        """
        Create a new instance of `perplexipy.PerplexityClient` using the API
        `key` to connect to the corresponding `endpoint`.

        Arguments
        ---------
            key
        A valid API key string.  If not present, it defaults to `perplexipy.PERPLEXITY_API_KEY`.

            endpoint
        A string representing a URL to the Perplexity API.

            unitTest
        A Boolean to indicate if internal object states need to be modified for
        unit testing.  Has no effect in regular code.

        Returns
        -------
        An instance of `perplexipy.PerplexityClient` if successful.

        Attributes:

        `model` - the current model to use in queries, user configurable.

        The role is fixed to `"user"` for Perplexity calls, per the API
        recommendations.

        Raises
        ------
            PerplexityClientError
        If the API key is empty, or doesn't match one of the valid API prefixes
        per the documentation.
        """
        if not key:
            raise PerplexityClientError('Provide a valid key argument during instantiation')
        if not PERPLEXITY_API_PREFIX in key:
            raise PerplexityClientError('The key %s is missing the pplx- prefix - invalid API key' % key)
        if not all(ord(' ') <= ord(c) <= ord('~') for c in key):
            raise PerplexityClientError('The key %s contains invalid characters' % key)

        self._endpoint = endpoint
        self._key = key
        self._role = PERPLEXITY_DEFAULT_ROLE
        self._model = PERPLEXITY_DEFAULT_MODEL
        self._client = OpenAI(
            api_key = self._key,
            base_url = self._endpoint,
            timeout = PERPLEXITY_TIMEOUT,
        )
        self._unitTest = unitTest


    def query(self, query: str) -> str:
        """
        Send a single message query to the service, receive a single response.

        Arguments
        ---------
            query
        A string with the query in one of the model's supported languages.

        Returns
        -------
        A string with a response from the Perplexity service.

        Raises
        ------
            Exception
        An `openai.BadRequestError` or similar if the query is malformed or has
        something other than text data.  The error raised passes through
        whatever the API raised.

        In most cases, the API returns `openai.BadRequestError`.

            PerplexityClientError
        If the query is `None` or empty.
        """
        if not query:
            raise PerplexityClientError('query cannot be None or empty')

        messages = [ { 'role': self._role, 'content': query, }, ]

        response = self._client.chat.completions.create(
            model = self.model,
            messages = messages,
            # TODO: check the OpenAI documentation to see how this is used.
            # See:  https://docs.mistral.ai/platform/guardrailing/
            # No guardrailing.
            # safe_mode = False,
        )

        result = response.choices[0].message.content

        return result


    def queryBatch(self, query: str) -> tuple:
        """
        Send a single message query to the service, receive a single response.

        Arguments
        ---------
            query
        A string with the query in one of the model's supported languages.

        Returns
        -------
        A tuple with a batch of 1 or more response strings.

        Raises
        ------
            Exception
        An `openai.BadRequestError` or similar if the query is malformed or has
        something other than text data.  The error raised passes through
        whatever the API raised.

        In most cases, the API returns `openai.BadRequestError`.

            PerplexityClientError
        If the query is `None` or empty.
        """
        if not query:
            raise PerplexityClientError('query cannot be None or empty')

        messages = [ { 'role': self._role, 'content': query, }, ]

        response = self._client.chat.completions.create(
            model = self.model,
            messages = messages,
        )

        result = tuple(choice.message.content for choice in response.choices)

        return result


    def queryStreamable(self, query: str) -> Responses:
        """
        Send a query and return a long, streamable response.

        Arguments
        ---------
            query
        A string with the query in one of the model's supported languages.

        Returns
        -------
        Returns a `perplexipy.Responses` object for streaming the textual
        responses from the client.  The response strips all metadata and returns
        only content strings, for simpler and easier integration.

        Raises
        ------
            Exception
        An `openai.BadRequestError` or similar if the query is malformed or has
        something other than text data.  The error raised passes through
        whatever the API raised.

        In most cases, the API returns `openai.BadRequestError`.

            PerplexityClientError
        If the query is `None` or empty.
        """
        if not query:
            raise PerplexityClientError('query cannot be None or empty')

        messages = [ { 'role': self._role, 'content': query, }, ]

        response = self._client.chat.completions.create(
            model = self.model,
            messages = messages,
            stream = True,
        )

        return Responses(response)


    @property
    def models(self, unitTest = False):
        """
        Provide a dictionary of the models supported by Perplexity listed in:

        https://docs.perplexity.ai/docs/model-cards

        Returns
        -------
        A dictionary of supported models as the key, with a `perplexypy.ModelInfo`
        named tuple with the model capabilities description.  The model
        information attributes are:

        - `parameterCount`
        - `contextLength`
        - `modelType`
        - `availability`
        """
        supportedModels = OrderedDict({
            'codellama-70b-instruct': ModelInfo('70B', 16384, 'chat completion', 'open source',),
            'llama-3-70b-instruct': ModelInfo('70B', 8192, 'chat completion', 'open source'),
            'llama-3-8b-instruct': ModelInfo('8B', 8192, 'chat completion', 'open source'),
            'llama-3-sonar-large-32k-chat': ModelInfo('8x7B', 32768, 'chat completion', 'Perplexity',),
            'llama-3-sonar-large-32k-online': ModelInfo('8x7B', 32768, 'chat completion', 'Perplexity',),
            'llama-3-sonar-small-32k-chat': ModelInfo('7B', 32768, 'chat completion', 'Perplexity',),
            'llama-3-sonar-small-32k-online': ModelInfo('7B', 32768, 'chat completion', 'Perplexity',),
            'mistral-7b-instruct': ModelInfo('7B', 16384, 'chat completion', 'open source',),
            'mixtral-8x7b-instruct': ModelInfo('8x7B', 16384, 'chat completion', 'open source',),
        })

        return supportedModels


    @property
    def model(self) -> str:
        """
        Return the model the client uses for requesting responses from the
        service provider.  Its default value is:  `PERPLEXITY_DEFAULT_MODEL`.
        """
        return self._model

    @model.setter
    def model(self, value: str):
        """
        Set the model to use for generating responses.

        Arguments
        ---------
            value
        A string matching one of the supported models.

        Returns
        -------
        `None` - setter method decorated as a property.

        Raises
        ------
        `perplexipy.PerplexityClientError` if the `value` isn't included in the list of
        supported models.
        """
        if not value:
            raise PerplexityClientError('value cannot be None')

        models = self.models
        if not self._unitTest:
            if value not in models:
                raise PerplexityClientError('value = %s error; supported models: %s' % (value, ', '.join(models)))

        self._model = value

        # Validate that the model still works, revert otherwise
        try:
            self.query('Concise answer: what color is the sky?')
        except:
            raise PerplexityClientError('model %s no longer available in underlying API')

