# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


__VERSION__ = '0.0.4'


from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

import os



PERPLEXITY_DEFAULT_MODEL = 'mistral-7b-instruct'
PERPLEXITY_DEFAULT_ROLE = 'user'
"""
`PERPLEXITY_API_KEY` is set to the environment variable of the same name if
present, otherwise it's set to the empty string `''`.
"""
PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY', default = '')
PERPLEXITY_API_URL = 'https://api.perplexity.ai'


class PerplexityClientError(Exception):
    """
    Perplexity client generic errors, for cleaner exception handling.
    """
    def __init__(self, errorMessage):
        super().__init__(errorMessage)


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
        self.model = PERPLEXITY_DEFAULT_MODEL
        self._client = OpenAI(api_key = self._key, base_url = self._endpoint)


    def query(self, query):
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
        """
        messages = [ { 'role': self._role, 'content': query, }, ]

        response = self._client.chat.completions.create(
            model = self.model,
            messages = messages,
        )

        result = response.choices[0].message.content

        return result

