"""This package stores parse tables created by ply for faster parsing of strings.

If any change is made to :py:mod:`backus_naur_parser` it is likely that these
tables do not reflect these changes until remade.

Remaking the tables can be done by removing the :code:`optimize=1` arguments in
the parser and lexer, and then running them in unoptimized python mode.
"""