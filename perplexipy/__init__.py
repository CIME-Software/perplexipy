# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


__VERSION__ = '0.0.6'


from collections import namedtuple

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

import os



"""
`PERPLEXITY_API_KEY` is set to the environment variable of the same name if
present, otherwise it's set to the empty string `''`.
"""
PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY', default = '')
PERPLEXITY_API_URL = 'https://api.perplexity.ai'
"""
The default model is **mistral-7b-instruct** because of it's efficiency and
performance qualities.  Ref:  https://arxiv.org/abs/2310.06825
"""
PERPLEXITY_DEFAULT_MODEL = 'mistral-7b-instruct'
PERPLEXITY_DEFAULT_ROLE = 'user'
PERPLEXITY_TIMEOUT = 30.0 # seconds


class PerplexityClientError(Exception):
    """
    Perplexity client generic errors, for cleaner exception handling.
    """
    def __init__(self, errorMessage):
        super().__init__(errorMessage)


class Responses:
    """
    Encapsulates all the streaming responses from a query and enables access to
    it using a purpose-built iterable.  Strips all the OpenAI response metadata
    and returns only the textual response.  It's a streaming iterable,
    open-ended.
    """
    def __init__(self, responsesStream):
        self._responsesStream = responsesStream


    def __iter__(self):
        return self


    def __next__(self):
        try:
            result = self._responsesStream.__next__().choices[0].delta.content
        except Exception as e:
            raise e
        return result


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
    def __init__(self, key = PERPLEXITY_API_KEY, endpoint = PERPLEXITY_API_URL):
        """
        Create a new instance of `perplexipy.PerplexityClient` using the API
        `key` to connect to the corresponding `endpoint`.

        Arguments
        ---------
            key
        A valid API key string.  If not present, it defaults to `perplexipy.PERPLEXITY_API_KEY`.

            endpoint
        An string representing a URL to the Perplexity API.

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
        if not 'pplx-' in key:
            raise PerplexityClientError('The key %s i missing the pplx- prefix - invalid API key')

        self._endpoint = endpoint
        self._key = key
        self._role = PERPLEXITY_DEFAULT_ROLE
        self._model = PERPLEXITY_DEFAULT_MODEL
        self._client = OpenAI(
            api_key = self._key,
            base_url = self._endpoint,
            timeout = PERPLEXITY_TIMEOUT,
        )


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
    def models(self):
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
        supportedModels = {
            'codellama-70b-instruct': ModelInfo('70B', 16384, 'chat completion', 'open source',),
            'mistral-7b-instruct': ModelInfo('7B', 16384, 'chat completion', 'open source',),
            'mixtral-8x7b-instruct': ModelInfo('8x7B', 16384, 'chat completion', 'open source',),
            'sonar-medium-chat': ModelInfo('8x7B', 16348, 'chat completion', 'Perplexity',),
            'sonar-medium-online': ModelInfo('8x7B', 12000, 'chat completion', 'Perplexity',),
            'sonar-small-chat': ModelInfo('7B', 16384, 'chat completion', 'Perplexity',),
            'sonar-small-online': ModelInfo('7B', 12000, 'chat completion', 'Perplexity',),
        }

        return supportedModels


    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str):
        """
        """
        models = self.models.keys()
        if value not in models:
            raise PerplexityClientError('value = %s error; supported models: %s' % (value, ', '.join(models)))

        self._model = value

