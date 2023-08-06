"""This module provides transformations for finite automata.

"""

from formgram.machines.finite_automata.classifiers import is_deterministic, find_epsilon_edges
from formgram.machines.finite_automata.simulation_functions import create_shortest_epsilon_route_map, \
    create_epsilon_hull
from formgram.machines.helper_functions.nested_dictionaries import create_nested_dict
from formgram.grammars.helper_functions.decorators import deepcopy_arguments
from formgram.grammars.helper_functions.set_functions import powerset


@deepcopy_arguments
def to_deterministic(machine: dict) -> dict:
    """Transform to a deterministic finite automaton

    :param machine: Any finite automaton
    :return: a new deterministic finite automaton
    """
    if is_deterministic(machine):
        return machine
    edge_dict = create_nested_dict(machine["edges"])
    node_powerset = powerset(machine["nodes"])
    accepting_powerset = {
        subset
        for subset in node_powerset
        if subset.intersection(machine["accepting_nodes"])
    }

    epsilon_map = create_shortest_epsilon_route_map(
        find_epsilon_edges(machine["edges"])
    )
    new_edges = {}
    for source_set in node_powerset:
        epsilon_hull = create_epsilon_hull(
            epsilon_route_map=epsilon_map, state_set=source_set
        )
        for symbol in machine["alphabet"]:
            reached = {
                target
                for node in epsilon_hull
                for target in edge_dict[node].get(symbol, default={})
            }
            target_set = create_epsilon_hull(
                epsilon_route_map=epsilon_map, state_set=reached
            )
            new_edges.add(
                (str(sorted(source_set)), symbol, str(sorted(target_set)))
            )

    return {
        "nodes": {str(sorted(subset)) for subset in node_powerset},
        "alphabet": machine["alphabet"],
        "edges": new_edges,
        "accepting_nodes": {str(sorted(subset)) for subset in accepting_powerset},
        "starting_nodes": {str(sorted(machine["starting_nodes"]))},
    }


@deepcopy_arguments
def to_unreachable_state_free_form(machine: dict) -> dict:
    """Remove all nodes from machine, which are not reachable from a starting node

    :param machine:
    :return: a new finite automaton without states unreachable from the starting node
    """
    reachables = {node for node in machine["starting_nodes"]}
    new_reached = reachables
    symbol_agnostic_edge_dict = create_nested_dict(
        {(source, target) for (source, _, target) in machine["edges"]}
    )
    while new_reached:
        last_reached = new_reached
        new_reached = set()
        for node in last_reached:
            new_reached.update(symbol_agnostic_edge_dict[node].difference(reachables))
            reachables.update(symbol_agnostic_edge_dict[node])
    machine["nodes"] = reachables
    machine["accepting_nodes"] = machine["accepting_nodes"].intersection(reachables)
    return machine
