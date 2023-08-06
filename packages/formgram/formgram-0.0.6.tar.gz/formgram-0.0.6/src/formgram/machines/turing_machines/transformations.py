"""This module provides transformations for Turing machines.

"""


from formgram.grammars.helper_functions.decorators import deepcopy_arguments
from formgram.grammars.helper_functions.set_functions import find_new_unique_string


@deepcopy_arguments
def to_grammar_transformable_form(machine: dict) -> dict:
    """Create equivalent Turing machine which writes a single one on acceptance

    The new machine works the same as the original until the original would halt
    accepting, in which case the whole tape is rewritten blank and a single "1"
    is written on it before it halts in accepting state.

    :param machine:
    :return: A new equivalent Turing machine
    """

    machine = rename_tape_symbol_intersecting_states(machine)

    machine = create_new_initial_state(machine)

    machine = replace_blank_symbol_transitions(machine)

    machine = modify_accepting_behaviour(machine)

    return machine


@deepcopy_arguments
def rename_tape_symbol_intersecting_states(machine: dict) -> dict:
    """Create equivalent Turing machine with renamed states which were also tape symbols

    :param machine:
    :return: A new equivalent Turing machine
    """
    tape_symbols = machine["alphabet"].union(machine["control_symbols"])
    state_symbols = machine["states"]
    intersecting_states = state_symbols.intersection(tape_symbols)
    for state_string in intersecting_states:
        machine["states"].remove(state_string)
        new_state_string = find_new_unique_string(
            tape_symbols.union(machine["states"]), state_string)
        machine["states"].add(new_state_string)
        if state_string == machine["initial_state"]:
            machine["initial_state"] = new_state_string
        if state_string in machine["accepting_states"]:
            machine["accepting_states"].remove(state_string)
            machine["accepting_states"].add(state_string)
    return machine


@deepcopy_arguments
def create_new_initial_state(machine: dict) -> dict:
    """Create equivalent Turing machine with new initial state

    The starting state only transitions to previous initial state.

    :param machine:
    :return: A new equivalent Turing machine
    """
    tape_symbols = machine["alphabet"].union(machine["control_symbols"])
    new_initial_state = find_new_unique_string(machine["states"], "START")
    old_initial_state = machine["initial_state"]
    machine["initial_state"] = new_initial_state
    for symbol in tape_symbols:
        new_start_transition = ((new_initial_state, symbol), (old_initial_state, symbol, "S"))
        machine["transitions"].add(new_start_transition)
    return machine


@deepcopy_arguments
def replace_blank_symbol_transitions(machine: dict) -> dict:
    """Create equivalent Turing machine without blank symbol writes

    This is done by:

    * Creating an alternate symbol
    * Replace all written blank symbols with this new symbol
    * Add new transitions reading the new symbol instead of the blank symbol
        in addition to the old blank reading transitions

    :param machine:
    :return: A new equivalent Turing machine
    """

    new_blank_like = find_new_unique_string(machine["control_symbols"], ".")
    machine["control_symbols"].add(new_blank_like)

    for transition in machine["transitions"]:
        (read_state, read_symbol), (write_state, write_symbol, move_direction) = transition
        if write_symbol == machine["blank_symbol"]:
            new_transition = ((read_state, read_symbol), (write_state, new_blank_like, move_direction))
            machine["transitions"].remove(transition)
            machine["transitions"].add(new_transition)

    # Ensure new blank like symbol has same functionality i.e. can be read as a blank
    for transition in machine["transitions"].copy():
        (read_state, read_symbol), (write_state, write_symbol, move_direction) = transition
        if read_symbol == machine["blank_symbol"]:
            new_transition = ((read_state, new_blank_like), (write_state, write_symbol, move_direction))
            machine["transitions"].add(new_transition)

    return machine


@deepcopy_arguments
def modify_accepting_behaviour(machine: dict) -> dict:
    """Create equivalent Turing machine with a clear tape state when accepting

    The new Turing machine will have an almost empty tape with only one "1"
    written on it when halting acceptingly.

    This is done by modifying the transitions of the given machine.

    :param machine:
    :return: An equivalent Turing machine
    """
    tape_symbols = machine["alphabet"].union(machine["control_symbols"])

    # Create new states for new subroutines
    goto_right_end_state = find_new_unique_string(machine["states"], "GOTO_RIGHT_END")
    machine["states"].add(goto_right_end_state)
    clear_tape_and_write_single_one_state = \
        find_new_unique_string(machine["states"], "CLEAR_TAPE_AND_WRITE_SINGLE_ONE")
    machine["states"].add(clear_tape_and_write_single_one_state)
    single_new_accepting_state = \
        find_new_unique_string(machine["states"], "NEW_AND_SINGLE_ACCEPTING_STATE")
    machine["states"].add(single_new_accepting_state)

    # Make new accepting state the only accepting state
    old_accepting_states = machine["accepting_states"]
    machine["accepting_states"] = {single_new_accepting_state}

    # Ensure there is a one in the tape symbols
    if "1" not in tape_symbols:
        machine["control_symbols"].add("1")
        tape_symbols.add("1")

    # all previously final states now go to GO_TO_RIGHT_END instead of halting
    for old_final_state in old_accepting_states:
        non_halting_symbols = {symbol for ((state, symbol), _) in machine["transitions"] if state == old_final_state}
        halting_symbols = tape_symbols.difference(non_halting_symbols)
        for symbol in halting_symbols:
            machine["transitions"].add(
                ((old_final_state, symbol),
                 (goto_right_end_state, symbol, "R"))
            )

    # add rules for GO_TO_RIGHT_END
    for symbol in tape_symbols:
        if symbol == machine["blank_symbol"]:
            machine["transitions"].add(
                ((goto_right_end_state, symbol),
                 (clear_tape_and_write_single_one_state, symbol, "L"))
            )
        else:
            machine["transitions"].add(
                ((goto_right_end_state, symbol),
                 (goto_right_end_state, symbol, "R"))
            )

    # add rules for CLEAR_TAPE_AND_WRITE_SINGLE_ONE
    for symbol in tape_symbols:
        if symbol == machine["blank_symbol"]:
            machine["transitions"].add(
                ((clear_tape_and_write_single_one_state, symbol),
                 (single_new_accepting_state, "1", "R"))
            )
        else:
            machine["transitions"].add(
                ((clear_tape_and_write_single_one_state, symbol),
                 (clear_tape_and_write_single_one_state, machine["blank_symbol"], "L"))
            )

    return machine
