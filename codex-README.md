% Codex(3) Version 1.0.4 | PerplexiPy command line code explainer

Name
====

**codex** - A command line code explainer and snippet generator based on
PerplexiPy.


<img src='https://images2.imgbox.com/57/94/AsI1WSfy_o.png'>


Synopsis
========
```bash
codex 'Show me how to instantiate a dataframe from a dictionary in Python'
```


Description
===========
**Codex** is an interactive command line tool for answering programming queries
related to coding and shell scripting.  It uses the Code Llama model to generate
its responses.

Response text is ready to run / ready to paste in most cases.  The output can
be imported into Vim or emacs buffers as-is.


Installation
============
**Codex** is installed as part of the PerplexiPy API package.

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
# In a virtualenv:
pip install -U perplexipy
export PERPLEXITY_API_KEY="your-key-goes-here"
codex repl
```

Starts a REPL playground for continuous interaction during a command line
session.  The REPL can be interrupted at any time with `Ctrl-C` and it follows
all shell and REPL behavior best practices.

Commands:

- `/active [modelID]` display the current active model or set the active model
  to `modelID`, where the latter is the number of model in the `/models` listing
- `/cinfo` display configuration info
- `/clear` clear the screen before the next prompt
- `/help` this list of commands help
- `/mode [mode]` display or set the editing mode to `vi` or `emacs`
- `/models` list available models; ordinal ::= `modelID` for `/active`
- `/style` display or set the query style as `code` or `human`
- '/version' display the PerplexiPy + Codex version

The REPL starts in `vi` or `Vim` editing mode by default.  Use `/active emacs`
to override.

When `/style` is set to `code`, all queries are forced to be related to
programming, scripting, or system administration.  When it's set to `human` the
queries are "general purpose human information" and may return free form
responses.

Sample session:

<a href='https://images2.imgbox.com/c4/de/6kQ4aDuA_o.png' target='_blank'>
    <img src='https://images2.imgbox.com/c4/de/6kQ4aDuA_o.png'>
</a>


Command line usage:

```bash
codex 'A coding question here; best if the language is specified.'
```

The coding question, including any code snippets, must be enclosed in single
quotes to prevent shell expansion in Unix-like systems.

**Codex** can also process input provided from stdin through redirection or a
pipe:


```bash
echo "How do I reverse a string in Java?" | codex
```

The output always goes to stdout.  This simplifies integration with editors and
IDEs that support a streaming interface like Vim, emacs, VS Code, etc.


Vim
---
Use the `:h read` Vim command to run **Codex** and insert its output at the
current cursor position:

```vim
:read !codex 'Python pandas dataframe declaration using a dictionary defined by x'
```

Visual mode selections can be passed to **Codex** as snippets for analysis or
explanation.


License
=======
**Codex**, the **PerplexiPy** package, documentation and examples are licensed
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


