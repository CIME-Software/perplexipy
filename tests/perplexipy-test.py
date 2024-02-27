# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt

from perplexipy import PerplexityClient
from perplexipy import PerplexityClientError

import pytest


def test_PerplexityClient():
    with pytest.raises(PerplexityClientError):
        PerplexityClient(None)
    with pytest.raises(PerplexityClientError):
        PerplexityClient('')
    with pytest.raises(PerplexityClientError):
        PerplexityClient('xxxx')



