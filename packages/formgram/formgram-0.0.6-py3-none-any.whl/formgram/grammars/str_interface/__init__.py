"""This package uses yacc to parse strings into grammar dicts.

The strings must be in a specific modification of the Backus Naur form.

Rules:

    * Nonterminals must be wrapped in brackets like: `<Nonterminal>`
    * Terminals must be wrapped in quotations like: `'Terminal symbol'`
    * Left and right side of each production are separated by `::=`
    * Only one left side per line
    * Multiple right hand sides with same left hand side per line are to be separated by `|`
    * Empty right hand sides are allowed
    * The first line may only have the starting symbol as the left hand side
    * Everything after the `#` symbol in a line is a comment and will be ignored
    * Whitespace will be ignored, except for signaling end of line

:example:
    >>> grammar_string = ''' # comments look like this and are permitted in the string
    >>> <START> ::= <A> | 's' <START>
    >>> 's''s'<A> ::= 's'<A>'s'
    >>> <A> ::= <START> <START>
    >>> 's'<A>'s' ::= 'a'
    >>> <A> ::=  # this is an epsilon rule
    >>> '''
    >>> grammar = parse(grammar_string)
    >>> grammar
    {
        "terminals": {"s", "a"},
        "nonterminals": {"START", "A"},
        "productions": {
            (("START", ), ("A", )),
            (("START", ), ("s", "START")),
            (("s", "s", "A"), ("s", "A", "s")),
            (("A", ), ("START", "START")),
            (("s", "A", "s"), ("a", )),
            (("A", ), ())
        },
        "starting_symbol": "START"
    }
"""


from formgram.grammars.str_interface.backus_naur_parser import parse
