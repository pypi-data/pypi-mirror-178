"""This module provides functions to simulate any given pushdown automaton.

For the structure of those automata look at the package description.

The runtime description of the pushdown automaton consists of stack and state.


"""

from typing import Sequence, Tuple, Set

from formgram.machines.pushdown_automata.grammar_interface import nest_push_down_automata_transitions


def simulate_single_epsilon_step(transition_dict: dict, current_state: str, stack: Tuple[str]) -> Set[Tuple[str, Tuple[str]]]:
    """Return set of all states reachable in exactly one epsilon transition from a single state

    :param transition_dict:
    :param current_state:
    :param stack:
    :return: set of all directly epsilon reachable state, stack tuples
    """
    if not stack:
        return set()
    stack_head, *stack_tail = stack
    options = transition_dict.get(current_state, {}).get(None, {}).get(stack_head, set())
    return {
        (new_state, (insert_to_stack if insert_to_stack else ()) + tuple(stack_tail))
        for (new_state, insert_to_stack) in options
    }


def simulate_arbitrary_epsilon_steps(transition_dict: dict, combinations: set) -> set:
    """Return set of all states reachable by any amount of epsilon transitions from a collection of states

    :param transition_dict:
    :param combinations:
    :return: set of all epsilon reachable state, stack tuples
    """
    reached_combinations = combinations.copy()
    unexplored_combinations = combinations.copy()
    while unexplored_combinations:
        _state, _stack = unexplored_combinations.pop()
        new_combinations = simulate_single_epsilon_step(
            transition_dict, _state, _stack
        ).difference(reached_combinations)
        unexplored_combinations.update(new_combinations)
        reached_combinations.update(new_combinations)
    return reached_combinations


def simulate_single_symbol_step(transition_dict: dict, current_state: str, read_symbol: str, stack: Tuple[str]) -> set:
    """Return set of states reachable by reading exactly one symbol from a single state

    :param transition_dict:
    :param current_state:
    :param read_symbol:
    :param stack:
    :return: set of state, stack tuples reachable by exactly one symbol transition
    """
    if not stack:
        return set()
    stack_head, *stack_tail = stack
    options = (
        transition_dict.get(current_state, {}).get(read_symbol, {}).get(stack_head, set())
    )
    return {
        (new_state, (insert_to_stack if insert_to_stack else ()) + tuple(stack_tail))
        for (new_state, insert_to_stack) in options
    }


def simulate_single_step(transition_dict: dict, combinations: set, read_symbol: str) -> set:
    """Return set of states reachable by one symbol and arbitrary epsilon transitions from a collection of states

    :param transition_dict:
    :param combinations:
    :param read_symbol:
    :return: set of reachable state, stack tuples by given symbol transition and arbitrary epsilon transitions
    """
    epsilon_hull = simulate_arbitrary_epsilon_steps(transition_dict, combinations)
    single_symbol_step = {
        combination
        for state, stack in epsilon_hull
        for combination in simulate_single_symbol_step(
            transition_dict, state, read_symbol, stack
        )
    }
    return simulate_arbitrary_epsilon_steps(transition_dict, single_symbol_step)


def run_full_simulation(machine: dict, input_tape: Sequence[str], state_accepting: bool = False) -> bool:
    """Simulate pushdown automaton on input tape

    :param machine:
    :param input_tape:
    :param state_accepting: if True automaton accepts by state, else by stack
    :return: True if input_tape is accepted by automaton
    """
    transition_dict = nest_push_down_automata_transitions(machine["transitions"])
    options = simulate_arbitrary_epsilon_steps(
        transition_dict,
        {(machine["starting_state"], (machine["initial_stack_symbol"],))},
    )
    for symbol in input_tape:
        options = simulate_single_step(transition_dict, options, symbol)

        if not options:
            return False
    if state_accepting:
        for (state, _) in options:
            if state in machine["accepting_states"]:
                return True
        return False
    else:
        for (_, stack) in options:
            if not stack:
                return True
        return False
