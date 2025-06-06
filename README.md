% perplexipy(3) Version 1.3.1 | Perplexity AI high level API documentation

Name
====

**PerplexiPy** - Perplexity AI high level library


<img src='https://images2.imgbox.com/57/94/AsI1WSfy_o.png'>


Synopsis
========
```python
client = PerplexityClient() \
print(client.query('What is the meaning of 42?') \
for result in client.queryStreamable('List of all US presidents'): \
    print(result)
```


Description
===========
**PerplexiPy** is a high-level, convenience library for interacting with the
Perplexity API from any Python 3.9+ application.  The library aims to simplify
interactions with Perplexity models by encapsulating all the implementation
details of the lower level OpenAI API.  All interaction between the code and
this library occurs in the form of string and native Python objects, not
OpenAPI / Swagger mapped objects.

**PerplexiPy** implements a combination of the Perplexity AI and the
OpenAI outputs.  API semantics follow the "literate programming" workflow,
and attempt to make the resulting code as simple to follow as possible.

<a href='https://www.perplexity.ai/' target='_blank'>Perplexity AI</a> is an
AI-powered search engine that uses natural language
processing and machine learning to provide accurate and comprehensive answers to
end-user queries.  It can be argued that it outperforms OpenAI's offerings in
accuracy and responsiveness.  **PerplexiPy** enables the creation of Python
programs and tools that leverage the power of Perplexity AI.


Documentation
=============
These documents encompass all information about **PerplexiPy**:

- This README file, hosted in the **[perplexipy](https://github.com/CIME-Software/perplexipy)** GitHub repository
  project on GitHub and exported to the PyPI project page
- A `man` page autogenerated from this README file, `perplexipy.3`
- The complete **PerplexiPy API reference** on GitHub Pages - https://cime-software.github.io/perplexipy/perplexipy.html
- The <a href='https://github.com/CIME-Software/perplexipy/blob/master/PerplexiPy-tutorial.ipynb' target='_blank'>PerplexiPy-tutorial.ipynb</a> tutorial notebook

The `man` page can be generated from the source distribution using this command:

```bash
make manpage
```

The output will reside in:  `./manpages/perplexipy.3`.  The `man` page isn't
included in the Python package wheel because there's no accepted standard
installation that's cross-compatible among all supported operating systems and
distributions.


Installation
============
```bash
pip install perplexipy
```

Package information:  https://pypi.org/project/perplexipy

PerplexiPy requires an API key issued by Perplexity.  You may set PERPLEXITY_API_KEY
as an environment variable or use a `.env` file.


API key
=======
Access to the Perplexity API requires a paid subscription and an API key.

Use of `.env` is recommended for storing the private key.  There is an automatic
constant `PERPLEXITY_API_KEY` that gets initialized to the value of a `.env` key
of the same name via the `dotenv` API.  Otherwise, `PERPLEXITY_API_KEY` may
be handled like any other secret by the implementing team.  This module provides
no other tools or services for handling the API key.

This key is used only during `PerplexityClient` instantiation:

```python
import os

key = os.environ['PERPLEXITY_API_KEY']
client = PerplexityClient(key = key)
print(client.query('Brief answer:  greet the world in Swedish.'))
```


Usage
=====
See the <a href='https://github.com/CIME-Software/perplexipy/blob/master/PerplexiPy-tutorial.ipynb' target='_blank'>PerplexiPy-tutorial.ipynb</a> notebook for a richer example of the API's
capabilities.

In general:

```python
client = PerplexityClient()
result = client.query('Show me how to declare a list in Python')
# result is a string

results = client.queryBatch('Show me different ways of declaring a Python list')
for result in results:
    print(result)
    # results is a tuple of one or more results

results = client.queryStreamable('Tell me why lists are important in programming')
for result in results:
    print(result)
    # results is a long stream of data, served over time.

models = client.models # lists all models supported by Perplexity AI

print('Model names:')
for model in models.keys():
    print(' - %s' % model)

try:
    client.model = 'bogus-LLM-7b'
except PerplexityClientError as e:
    print(e)

client.model = models.keys()[0] # OK
```


Async usage
===========
Not supported at this time.


Interactive usage
=================
PerplexiPy ships with the Codex Playground, an interactive REPL console.  To
run it:

```bash
# In a virtualenv:
pip install -U perplexipy
export PERPLEXITY_API_KEY="your-key-goes-here"
codex repl
```

Full description of Codex Playground and other use cases like streaming API and
CLI argument passing in the [Codex README](https://github.com/CIME-Software/perplexipy/blob/master/codex-README.md).


License
=======
The **PerplexiPy** package, documentation and examples are licensed under the
[BSD-3 open source license](https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt).


See also
========
- **codex** - a PerplexiPy command line code explainer
- API documentation:  https://cime-software.github.io/perplexipy
- <a href='https://www.perplexity.ai/' target='_blank'>Perplexity AI</a>
- m0toko:  a Sopel bot plug-in that uses PerplexiPy for providing AI-enhanced
  chatbot functionality:  https://github.com/pr3d4t0r/m0toko
- PyPI:  <a href='https://pipy.org/project/openai' target='_blank'>openai</a>


Caveats
=======
The code should work with Python 3.7 or later, but it was only tested with
Python 3.9.16 and later.  Download the package and install it from source if
support for an earlier Python version is required.


Bugs
====
Feature requests and bug reports:

https://github.com/CIME-Software/perplexipy/issues

