# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


__VERSION__ = '0.0.2'


import os

import requests


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
        An instance of `perplexipy.PerplexityClient` if successful.  The
        API service endpoint isn't validated until the first call to get a
        response.

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

        self._key = key
        self._endpoint = endpoint

