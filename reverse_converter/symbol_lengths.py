#!/usr/bin/python3.10
"""Script containing internal representations of symbol-length .

Primarily used for compatibility with music21 library.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import logging

import music21 as music


# SYMBOL_TO_LENGTH = {
#     'hundred_twenty_eighth': 0.03125,  # '128th',
#     'sixty_fourth': 0.0625,  # '64th',
#     'thirty_second': 0.125,  # '32th',
#     'sixteenth': 0.25,  # '16th',
#     'eighth': 0.5,  # 'eighth',
#     'quarter': 1,  # 'quarter',
#     'half': 2,  # 'half',
#     'whole': 4,  # 'whole',
#     'double_whole': 2*4,
#     'quadruple_whole': 4*4
# }

SYMBOL_TO_LENGTH = {
    'hundred_twenty_eighth': 0.03125,
    'hundred_twenty_eighth.': 0.046875,
    'hundred_twenty_eighth..': 0.0546875,
    'sixty_fourth': 0.0625,
    'sixty_fourth.': 0.09375,
    'sixty_fourth..': 0.109375,
    'thirty_second': 0.125,
    'thirty_second.': 0.1875,
    'thirty_second..': 0.21875,
    'sixteenth': 0.25,
    'sixteenth.': 0.375,
    'sixteenth..': 0.4375,
    'eighth': 0.5,
    'eighth.': 0.75,
    'eighth..': 0.875,
    'quarter': 1.0,
    'quarter.': 1.5,
    'quarter..': 1.75,
    'half': 2.0,
    'half.': 3.0,
    'half..': 3.5,
    'whole': 4.0,
    'whole.': 6.0,
    'whole..': 7.0,
    'double_whole': 8.0,
    'double_whole.': 12.0,
    'double_whole..': 14.0,
    'quadruple_whole': 16.0,
    'quadruple_whole.': 24.0,
    'quadruple_whole..': 28.0
}


def label_to_length(length: str) -> music.duration.Duration:
    """Return length of label as music21 duration.

    Args:
        length (str): only length part of one label in semantic format as string

    Returns:
        music.duration.Duration: one duration in music21 format
    """
    # dots = 0
    # while length.endswith('.'):
    #     dots += 1
    #     length = length[:-1]

    if length in SYMBOL_TO_LENGTH:
        return music.duration.Duration(SYMBOL_TO_LENGTH[length])  # , dots=dots)
    else:
        logging.info(f'Unknown duration label: {length}, returning default duration.')
        return music.duration.Duration(1)


def length_to_label(length: float) -> str:
    """Given length in quarterNotes, return length-label as semantic format.

    Args:
        length (float): length in quarter notes

    Returns:
        str: only length part of one label in semantic format as string
    """


    #
    # if length.dots == 0:
    #     return SYMBOL_TO_LENGTH[length.quarterLength]
    # else:
    #     return SYMBOL_TO_LENGTH[length.quarterLength] + '.' * length.dots