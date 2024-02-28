# See: https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt


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

