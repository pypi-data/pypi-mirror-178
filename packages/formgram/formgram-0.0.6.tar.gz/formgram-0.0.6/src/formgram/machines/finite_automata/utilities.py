"""This module provides interfaces to graphviz and jove.

"""
from typing import Union

import graphviz

from formgram.grammars.helper_functions.decorators import deepcopy_arguments
from formgram.grammars.helper_functions.set_functions import find_new_unique_string


@deepcopy_arguments
def to_jove(machine: dict) -> dict:
    """Create a dictionary as needed by the jove package

    :param machine:
    :return: A jove compliant dictionary for finite automata
    """
    epsilon = ""
    if epsilon in machine["alphabet"]:
        raise ValueError("The empty string is needed by jove as epsilon, and can not be in the alphabet")

    jove_delta = {}
    for node, symbol, target_node in machine["edges"]:
        if symbol is None:
            symbol = epsilon  # jove handles epsilon in a different way than grammars
        key = (node, symbol)
        if key in jove_delta:
            jove_delta[key].add(target_node)
        else:
            jove_delta[key] = {target_node}

    return {
        "Q": machine["nodes"],
        "Sigma": machine["alphabet"],
        "Q0": machine["starting_nodes"],
        "Delta": jove_delta,
        "F": machine["accepting_nodes"]
    }


@deepcopy_arguments
def to_dot(machine: dict, as_object: bool = False) -> Union[graphviz.Digraph, str]:
    """Create a dot language string for a graphical representation of the finite automaton

    :param as_object: If True, the function will return a graphviz Digraph
        instead of a dot language string
    :param machine:
    :return: Either a graphviz object or a string representing it depending on `as_object`
    """
    graph = graphviz.Digraph()
    pre_start_node_name = find_new_unique_string(previous_symbols=machine["alphabet"] | machine["nodes"],
                                                 string_base="pre_start")
    graph.node(pre_start_node_name, shape="point")

    for accepting_node in machine["accepting_nodes"]:
        graph.node(accepting_node, shape="doublecircle")
    for normal_node in machine["nodes"] - machine["accepting_nodes"]:
        graph.node(normal_node, shape="circle")
    for source, symbol, target in machine["edges"]:
        graph.edge(source, target, label=f"{symbol}")
    for starting_node in machine["starting_nodes"]:
        graph.edge(pre_start_node_name, starting_node)

    if as_object:
        return graph
    else:
        return graph.source
