# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


__VERSION__ = '0.0.1'


import requests


PERPLEXITY_API_URL = 'https://api.perplexity.ai'


class PerplexityClientError(Exception):
    def __init__(self, errorMessage):
        super().__init__(errorMessage)


class PerplexityClient:
    def __init__(self, key, endpoint = PERPLEXITY_API_URL):
        if not key:
            raise PerplexityClientError('Provide a valid key argument during instantiation')
        if not 'pplx-' in key:
            raise PerplexityClientError('The key %s i missing the pplx- prefix - invalid API key')

        self._key = key
        self._endpoint = endpoint

