#!/usr/bin/python3.10
"""Script for converting semantic sequential representation of music labels (produced by the model) to music21 stream
usable by music21 library to export to other formats.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import re
from enum import Enum
import logging

import music21 as music
from symbol import Symbol, SymbolType


def semantic_to_music21(labels: str) -> music.stream:
    """Converts labels to music21 format.

    Args:
        labels (str): one line of labels in semantic format without any prefixes.
    """
    labels = labels.strip('"')

    measures_labels = re.split(r'\s\+\sbarline\s\+\s', labels)
    measures = [Measure(measure_label) for measure_label in measures_labels if measure_label]

    logging.debug('Printing measures:')
    for measure in measures:
        print(measure)

    # TODO Go through all measures and convert Note objects to Music21 objects

    DEFAULT_RETURN_VALUE = music.stream.Stream([music.note.Note('C4', type='half'),
                                                music.note.Note('D4', type='half'),
                                                music.note.Note('E')])
    return DEFAULT_RETURN_VALUE


class Measure:
    _is_polyphonic = None

    def __init__(self, labels: str):
        """Takes labels corresponding to a single measure."""
        self.labels = labels
        self.keysignature = None

        label_groups = re.split(r'\s\+\s', self.labels.strip(''))
        self.label_groups = [SymbolGroup(label_group) for label_group in label_groups if label_group]

    @property
    def is_polyphonic(self) -> bool:
        """Returns True if there are more than 1 notes in the same label_group with different lengths."""
        if self._is_polyphonic is not None:
            return self._is_polyphonic

        # TODO: test this logic
        self._is_polyphonic = any(group.type == SymbolGroupType.TUPLE for group in self.label_groups)
        return self._is_polyphonic

    def __str__(self):
        label_groups_str = '\n'.join([str(group) for group in self.label_groups])
        poly = 'polyphonic' if self.is_polyphonic else 'monophonic'
        return (f'MEASURE: ({poly}) \n'
                f'labels: {self.labels}\n'
                f'{label_groups_str}')


class SymbolGroupType(Enum):
    SYMBOL = 0
    CHORD = 1
    TUPLE = 2
    EMPTY = 3
    UNKNOWN = 99


class SymbolGroup:
    """Represents one label group in a measure. Consisting of 1 to n labels/symbols."""

    def __init__(self, labels: str):
        self.labels = labels
        self.type = SymbolGroupType.UNKNOWN

        label_group_parsed = re.split(r'\s', self.labels.strip(''))
        self.symbols = [Symbol(label_group) for label_group in label_group_parsed if label_group]

        self.type = self.get_type()

    def __str__(self):
        symbols_str = '\n'.join([str(symbol) for symbol in self.symbols])
        return (f'\t({self.type}) {self.labels} =>\n'
                f'{symbols_str}')

    def get_type(self):
        if len(self.symbols) == 0:
            logging.warning(f'No symbols found in label group: {self.labels}')
            return SymbolGroupType.UNKNOWN
        if len(self.symbols) == 1:
            return SymbolGroupType.SYMBOL
        else:
            same_length = all(symbol.get_length() == self.symbols[0].get_length()
                              for symbol in self.symbols)

            return SymbolGroupType.CHORD if same_length else SymbolGroupType.TUPLE
