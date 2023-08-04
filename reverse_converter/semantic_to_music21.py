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
    measures_labels = [measure_label.strip() for measure_label in measures_labels if measure_label]

    if re.match(r'.*\s\+\sbarline$', measures_labels[-1]):
        measures_labels[-1] = measures_labels[-1][:-len(' + barline ')]

    measures = [Measure(measure_label) for measure_label in measures_labels if measure_label]

    previous_measure_key = None
    for measure in measures:
        previous_measure_key = measure.get_key(previous_measure_key)

    logging.debug('Printing measures:')
    for measure in measures:
        print(measure)

    DEFAULT_RETURN_VALUE = music.stream.Stream([music.note.Note('C4', type='half'),
                                                music.note.Note('D4', type='half'),
                                                music.note.Note('E')])
    return DEFAULT_RETURN_VALUE


class Measure:
    _is_polyphonic = None
    keysignature = None

    def __init__(self, labels: str):
        """Takes labels corresponding to a single measure."""
        self.labels = labels

        label_groups = re.split(r'\s\+\s', self.labels)
        self.symbol_groups = [SymbolGroup(label_group) for label_group in label_groups if label_group]

    def __str__(self):
        label_groups_str = '\n'.join([str(group) for group in self.symbol_groups])
        poly = 'polyphonic' if self.is_polyphonic else 'monophonic'
        return (f'MEASURE: ({poly}) \n'
                f'key signature: {self.keysignature}\n'
                f'labels: {self.labels}\n'
                f'{label_groups_str}')

    @property
    def is_polyphonic(self) -> bool:
        """Returns True if there are more than 1 notes in the same label_group with different lengths."""
        if self._is_polyphonic is not None:
            return self._is_polyphonic

        self._is_polyphonic = any(group.type == SymbolGroupType.TUPLE for group in self.symbol_groups)
        return self._is_polyphonic

    def get_key(self, previous_measure_key: music.key.Key) -> music.key.Key:
        """Returns the key of the measure.

        Args:
            previous_measure_key (music.key.Key): key of the previous measure.

        Returns:
            music.key.Key: key of the current measure.
        """
        if self.keysignature is not None:
            return self.keysignature

        for symbol_group in self.symbol_groups:
            key = symbol_group.get_key()
            print(key)
            if key is not None:
                self.set_key(key)
                break
        else:
            self.set_key(previous_measure_key)
        return self.keysignature

    def set_key(self, key: music.key.Key):
        """Sets the key of the measure. Send key to all symbols groups to represent notes in real height.

        Args:
            key (music.key.Key): key of the current measure.
        """
        self.keysignature = key
        for symbol_group in self.symbol_groups:
            symbol_group.set_key(key)


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

        label_group_parsed = re.split(r'\s', self.labels.strip())
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

    def get_key(self) -> music.key.Key | None:
        """Go through all labels and find key signature or return None.

        Returns:
            music.key.Key: key signature of the label group or None.
        """
        if not self.type == SymbolGroupType.SYMBOL:
            return None

        for symbol in self.symbols:
            if symbol.type == SymbolType.KEY_SIGNATURE:
                return symbol.repr

        return None

    def set_key(self, key):
        for symbol in self.symbols:
            symbol.set_key(key)
