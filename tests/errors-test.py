# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


from perplexipy.errors import PerplexityClientError


# +++ tests +++

def test_PerplexityClientError():
    e = PerplexityClientError('This is a test')

    assert str(e) == 'This is a test'

