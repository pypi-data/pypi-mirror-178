============
Formgram
============

|PyPI download month| |PyPI pyversions| |PyPI license|  |PyPI status|

**Formgram** is a toolkit for teaching and or learning formal grammars with a focus
on exploring the code and experimenting with and on it.

Students can use it to verify their findings in exercise problems and to understand
taught algorithms by looking at their implemented form *(and experimenting on them to see where
those might break)*.

Teachers can use it to teach algorithms in their implemented form as an alternative to
pure mathematical pseudocode.

>>> from formgram.classes.grammar import Grammar
>>> grammar_string = \
>>> """ # A simple context free grammar
>>> <Sentence> ::= <Subject> " " <Verb> " " <Object>
>>> <Subject> ::= <Noun>
>>> <Object> ::= <Noun>
>>> <Verb> ::= "bites" | "adores"
>>> <Noun> ::= "Human" | "Dog" | "Cat"
>>> """
>>> grammar = Grammar.from_str(grammar_string)
>>> type(grammar)
formgram.classes.grammar.ContextFreeGrammar



------------------------------------------
Installing Formgram and Supported Versions
------------------------------------------
Formgram is available on PyPI:

``$ python -m pip install formgram``

Formgram is written and tested on Python 3.8 and should work on any later version.

--------
Features
--------
Formgram is created to enable working with formal grammars in context of
a lecture on formal languages.
It can:

* Determine Chomsky hierarchy level
* Determine grammar normal forms
* Import/export grammars to string format
* Transform to and from corresponding machines

-----------------------------------------------------------------------------------------------------------
API Reference and User Guide available on `gwdg pages <https://theodor.moeser.pages.gwdg.de/formgram2022>`_
-----------------------------------------------------------------------------------------------------------

.. |PyPI download month| image:: https://pepy.tech/badge/formgram/month
    :target: https://pepy.tech/project/formgram

.. |PyPI license| image:: https://img.shields.io/pypi/l/formgram.svg
    :target: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/formgram.svg
    :target: https://pypi.python.org/pypi/formgram/

.. |PyPI status| image:: https://img.shields.io/pypi/status/formgram.svg
    :target: https://pypi.python.org/pypi/formgram/
