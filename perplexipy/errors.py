# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


class PerplexityClientError(Exception):
    """
    Perplexity client generic errors, for cleaner exception handling.
    """
    def __init__(self, errorMessage):
        super().__init__(errorMessage)



