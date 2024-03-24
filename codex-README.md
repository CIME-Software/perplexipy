% codex(1) Version 0.2.1 | PerplexiPy command line code explainer

Name
====

**codex** - A command line code explainer and snippet generator based on
PerplexiPy


Synopsis
========
```bash
codex 'Show me how to instantiate a dataframe from a dictionary in Python'
```


Description
===========
**codex** is an interactive command line tool for answering programming queries
related to coding and shell scripting.  It uses the Code Llama model to generate
its responses.

Response text is ready to run / ready to paste in most cases.  The output can
be imported into Vim or emacs buffers as-is.


Installation
============
**codex** is installed as part of the PerplexiPy API package.

```bash
pip install -U perplexipy
```

To check if it's installed, execute:

```bash
which codex
```

It should return something like `/usr/local/bin/codex`.


Usage
=====

```bash
codex 'A coding question here; best if the language is specified.'
```

The coding question, including any code snippets, must be enclosed in single
quotes to prevent shell expansion in Unix-like systems.


Vim
---
Use the `:h read` Vim command to run **codex** and insert its output at the
current cursor position:

```vim
:read !codex 'Python pandas dataframe declaration using a dictionary defined by x'
```

Visual mode selections can be passed to **codex** as snippets for analysis or
explanation.


License
=======
**codex**, the **PerplexiPy** package, documentation and examples are licensed
under the [BSD-3 open source license](https://github.com/CIME-Software/perplexipy/blob/master/LICENSE.txt).


See also
========
- PyPI:  <a href='https://pipy.org/project/perplexipy' target='_blank'>PerplexiPy</a>
- API documentation:  https://cime-software.github.io/perplexipy
- <a href='https://www.perplexity.ai/' target='_blank'>Perplexity AI</a>


Caveats
=======
The code should work with Python 3.7 or later, but it was only tested with
Python 3.9.16 and later.  Download the package and install it from source if
support for an earlier Python version is required.


Bugs
====
Feature requests and bug reports:

https://github.com/CIME-Software/perplexipy/issues


