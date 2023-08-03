#!/usr/bin/python3.10
"""Script containing Symbol class capable of representing Semantic label as other formats.

Primarily used for compatibility with music21 library.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import logging
from enum import Enum
import re

import music21 as music
from internal_symbols import Note, MultiRest, Tie


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
        self.length = self.get_length()

    def __str__(self):
        return f'\t\t\t({self.symbol_type}) {self.symbol}'

    def get_length(self) -> int:
        if self.symbol_type in [SymbolType.REST, SymbolType.NOTE, SymbolType.GRACENOTE]:
            return self.symbol.duration.quarterLength
        else:
            return 0

    @staticmethod
    def label_to_symbol(label: str):  # -> (SymbolType, music.object):
        """Converts one label to music21 format.

        Args:
            label (str): one symbol in semantic format as string
        """
        if label.startswith("clef-"):
            label = label[len('clef-'):]
            return SymbolType.CLEF, Symbol.clef_to_symbol(label)
        elif label.startswith("gracenote-"):
            label = label[len('gracenote-'):]
            return SymbolType.GRACENOTE, Symbol.note_to_symbol(label, gracenote=True)
        elif label.startswith("keySignature-"):
            label = label[len('keySignature-'):]
            return SymbolType.KEY_SIGNATURE, Symbol.keysignature_to_symbol(label)
        elif label.startswith("multirest-"):
            label = label[len('multirest-'):]
            return SymbolType.MULTI_REST, Symbol.multirest_to_symbol(label)
        elif label.startswith("note-"):
            label = label[len('note-'):]
            return SymbolType.NOTE, Symbol.note_to_symbol(label)
        elif label.startswith("rest-"):
            label = label[len('rest-'):]
            return SymbolType.REST, Symbol.rest_to_symbol(label)
        elif label.startswith("tie"):
            label = label[len('tie'):]
            return SymbolType.TIE, Symbol.tie_to_symbol(label)
        elif label.startswith("timeSignature-"):
            label = label[len('timeSignature-'):]
            return SymbolType.TIME_SIGNATURE, Symbol.timesignature_to_symbol(label)

        logging.info(f'Unknown label: {label}, returning None.')
        return SymbolType.UNKNOWN, None

    @staticmethod
    def clef_to_symbol(clef) -> music.clef:
        """Converts one clef label to music21 format.

        Args:
            clef (str): one symbol in semantic format as string

        Returns:
            music.clef: one clef in music21 format
        """
        if len(clef) != 2:
            logging.info(f'Unknown clef label: {clef}, returning default clef.')
            return music.clef.Clef()

        return music.clef.clefFromString(clef)

    @staticmethod
    def keysignature_to_symbol(keysignature) -> music.key.Key:
        """Converts one key signature label to music21 format.

        Args:
            keysignature (str): one symbol in semantic format as string

        Returns:
            music.key.Key: one key in music21 format
        """
        if not keysignature:
            logging.info(f'Unknown key signature label: {keysignature}, returning default key.')
            return music.key.Key()

        return music.key.Key(keysignature)

    @staticmethod
    def multirest_to_symbol(multirest: str) -> MultiRest:
        """Converts one multi rest label to internal MultiRest format.

        Args:
            multirest (str): one symbol in semantic format as string

        Returns:
            music.note.Rest: one rest in music21 format
        """
        def return_default_multirest() -> MultiRest:
            logging.info(f'Unknown multi rest label: {multirest}, returning default Multirest.')
            return MultiRest()

        if not multirest:
            return_default_multirest()

        try:
            return MultiRest(int(multirest))
        except ValueError:
            return return_default_multirest()

    @staticmethod
    def note_to_symbol(note, gracenote: bool = False) -> Note:  # -> Note:
        """Converts one note label to internal note format.

        Args:
            note (str): one symbol in semantic format as string
            gracenote (bool, optional): if True, returns grace note. Defaults to False.

        Returns:
            music.note.Note: one note in music21 format
        """
        def return_default_note() -> music.note.Note:
            logging.info(f'Unknown note label: {note}, returning default note.')
            return Note(music.duration.Duration(1), 'C4', gracenote=gracenote)

        if not note:
            return_default_note()

        note, fermata = Symbol.check_fermata(note)

        note_height, note_length = re.split('_', note, maxsplit=1)

        if not note_length or not note_height:
            return_default_note()

        return Note(Symbol.label_length(note_length),
                    note_height, fermata=fermata, gracenote=gracenote)

    @staticmethod
    def rest_to_symbol(rest) -> music.note.Rest:
        """Converts one rest label to music21 format.

        Args:
            rest (str): one symbol in semantic format as string

        Returns:
            music.note.Rest: one rest in music21 format
        """
        if not rest:
            logging.info(f'Unknown rest label: {rest}, returning default rest.')
            return music.note.Rest()

        rest, fermata = Symbol.check_fermata(rest)

        duration = Symbol.label_length(rest)

        rest = music.note.Rest()
        rest.duration = duration
        if fermata is not None:
            rest.expressions.append(fermata)

        return rest

    @staticmethod
    def tie_to_symbol(label):
        return Tie

    @staticmethod
    def timesignature_to_symbol(timesignature) -> music.meter.TimeSignature:
        """Converts one time signature label to music21 format.

        Args:
            timesignature (str): one symbol in semantic format as string

        Returns:
            music.meter.TimeSignature: one time signature in music21 format
        """
        if not timesignature:
            logging.info(f'Unknown time signature label: {timesignature}, returning default time signature.')
            return music.meter.TimeSignature()

        if timesignature == 'C/':
            return music.meter.TimeSignature('cut')
        else:
            return music.meter.TimeSignature(timesignature)

    @staticmethod
    def label_length(length: str) -> music.duration.Duration:
        """Return length of label as music21 duration.

        Args:
            length (str): only length part of one label in semantic format as string

        Returns:
            music.duration.Duration: one duration in music21 format
        """
        def return_default_duration():
            logging.info(f'Unknown duration label: {length}, returning default duration.')
            return music.duration.Duration(1)

        dots = 0
        while length.endswith('.'):
            dots += 1
            length = length[:-1]

        symbol_to_length = {
            'hundred_twenty_eighth': '128th',
            'sixty_fourth': '64th',
            'thirty_second': '32th',
            'sixteenth': '16th',
            'eighth': 'eighth',
            'quarter': 'quarter',
            'half': 'half',
            'whole': 'whole',
            'double_whole': 2*4,
            'quadruple_whole': 4*4
        }

        if length in symbol_to_length:
            return music.duration.Duration(symbol_to_length[length], dots=dots)
        else:
            return return_default_duration()

    @staticmethod
    def check_fermata(label: str) -> (str, music.expressions.Fermata):
        """Check if note has fermata.

        Args:
            label (str): one symbol in semantic format as string

        Returns:
            str: note without fermata
            music.expressions.Fermata: fermata
        """
        fermata = None
        if label.endswith('_fermata'):
            label = label[:-len('_fermata')]
            fermata = music.expressions.Fermata()
            fermata.type = 'upright'

        return label, fermata
