"""This module provides type aliases for argument annotations.

"""

from typing import Tuple, Set, Dict, Union

Symbol = str
Side = Tuple[Symbol, ...]
Word = Side
Production = Tuple[Side, Side]
Alphabet = Set[Symbol]
GrammarDict = Dict[str, Union[Symbol, Production, Alphabet]]
