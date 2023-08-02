#!/usr/bin/python3.10
"""Script containing Symbol class capable of representing Semantic label as other formats.

Primarily used for compatibility with music21 library.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import logging
from enum import Enum
import music21 as music


class SymbolType(Enum):
    NOTE = 0
    REST = 1
    CLEF = 2
    KEY_SIGNATURE = 3
    UNKNOWN = 99


class Symbol:
    """Represents one label in a label group."""
    def __init__(self, label: str):
        self.label_str = label
        self.symbol_type, self.symbol = Symbol.label_to_symbol(label)

    @staticmethod
    def label_to_symbol(label: str) -> (SymbolType, music.stream):
        """Converts one label to music21 format.

        Args:
            label (str): one symbol in semantic format as string
        """
        if label.startswith("note"):
            return SymbolType.NOTE, Symbol.note_to_symbol(label)
        elif label.startswith("rest"):
            return SymbolType.REST, Symbol.rest_to_symbol(label)
            # TODO: add other types of symbols here

        return SymbolType.UNKNOWN, None

    @staticmethod
    def note_to_symbol(label):
        return 'note'

    @staticmethod
    def rest_to_symbol(label):
        return 'rest'

    def __str__(self):
        return f'\t\t\t({self.symbol_type}) {self.symbol}'
