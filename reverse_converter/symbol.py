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
    CLEF = 0
    GRACENOTE = 1
    KEY_SIGNATURE = 2
    MULTI_REST = 3
    NOTE = 4
    REST = 5
    TIE = 6
    TIME_SIGNATURE = 7
    UNKNOWN = 99


class Symbol:
    """Represents one label in a label group."""
    def __init__(self, label: str):
        self.label_str = label
        self.symbol_type, self.symbol = Symbol.label_to_symbol(label)

    def __str__(self):
        return f'\t\t\t({self.symbol_type}) {self.symbol}'

    @staticmethod
    def label_to_symbol(label: str) -> (SymbolType, music.stream):
        """Converts one label to music21 format.

        Args:
            label (str): one symbol in semantic format as string
        """
        if label.startswith("clef"):
            return SymbolType.CLEF, Symbol.clef_to_symbol(label)
        elif label.startswith("gracenote"):
            return SymbolType.GRACENOTE, Symbol.gracenote_to_symbol(label)
        elif label.startswith("keySignature"):
            return SymbolType.KEY_SIGNATURE, Symbol.keysignature_to_symbol(label)
        elif label.startswith("multirest"):
            return SymbolType.MULTI_REST, Symbol.multirest_to_symbol(label)
        elif label.startswith("note"):
            return SymbolType.NOTE, Symbol.note_to_symbol(label)
        elif label.startswith("rest"):
            return SymbolType.REST, Symbol.rest_to_symbol(label)
        elif label.startswith("tie"):
            return SymbolType.TIE, Symbol.tie_to_symbol(label)
        elif label.startswith("timeSignature"):
            return SymbolType.TIME_SIGNATURE, Symbol.timesignature_to_symbol(label)

        return SymbolType.UNKNOWN, None



    @staticmethod
    def clef_to_symbol(label):
        return 'clef'

    @staticmethod
    def gracenote_to_symbol(label):
        return 'gracenote'

    @staticmethod
    def keysignature_to_symbol(label):
        return 'keySignature'

    @staticmethod
    def multirest_to_symbol(label):
        return'multirest'

    @staticmethod
    def note_to_symbol(label):
        return 'note'

    @staticmethod
    def rest_to_symbol(label):
        return 'rest'

    @staticmethod
    def tie_to_symbol(label):
        return 'tie'


    @staticmethod
    def timesignature_to_symbol(label):
        return 'timeSignature'
