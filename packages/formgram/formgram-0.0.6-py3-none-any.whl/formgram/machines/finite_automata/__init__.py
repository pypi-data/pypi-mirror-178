"""This package supplies functionality for finite automata.

* : A set
* starting_nodes: a subset of nodes set
* accepting_nodes: a subset of nodes set
* alphabet: a set
* edges: a set of tuples

Finite Automaton
==================
.. _fa description:

For this package a finite automaton is of type :class:`dict`

Keys
----

* nodes :class:`Set[str]`
    the set of all states
* accepting_nodes :class:`Set[str]`
    the subset of `states` which accept
* starting_nodes :class:`str`
    the element of `states` which is the internal state of the automaton when it is started
* alphabet :class:`Set[str]`
    the set of symbols from which the words can be created which are to be decided
* edges :class:`Set[Tuple[str, str | None, str]`
    the transition rules with which the automaton works.


Transitions
-----------

The transitions are ordered
``source_node, transition_symbol, target_node``
where

* source_node
    is element of ``nodes``
* transition_symbol
    is element of ``alphabet`` or ``None`` in case of an epsilon step
* target_state
    is element of ``nodes``


"""
