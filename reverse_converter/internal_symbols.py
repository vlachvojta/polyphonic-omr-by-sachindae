#!/usr/bin/python3.10
"""Script containing internal representations of symbols representing parsed semantic labels..

Primarily used for compatibility with music21 library.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import music21 as music


class Note:
    """Represents one note in a label group.

    In the order which semantic labels are represented, the real height of note depends on key signature
    of current measure. This class is used as an internal representation of a note before knowing its real height.
    Real height is then stored directly in `self.note` as music.note.Note object.
    """
    def __init__(self, duration: music.duration.Duration, height: str,
                 fermata: music.expressions.Fermata = None, gracenote: bool = False):
        self.duration = duration
        self.height = height
        self.fermata = fermata
        self.note = None
        self.gracenote = gracenote
        self.note_ready = False

    def get_real_height(self, key_signature: music.key.KeySignature):
        """Returns the real height of the note.

        :param key_signature: key signature of current measure
        :return: real height of the note
        """
        if self.note_ready:
            return self.note

        # TODO get real height from label height and key signature
        # self.note = ...
        # self.note_ready = True
        # return self.note
        return None

    def __str__(self):
        return f'note {self.height} {self.duration}'


class MultiRest:
    """Represents one multi rest in a label group."""
    def __init__(self, duration: int = 0):
        self.duration = duration


class Tie:
    """Represents one tie in a label group."""
    def __str__(self):
        return 'tie'
