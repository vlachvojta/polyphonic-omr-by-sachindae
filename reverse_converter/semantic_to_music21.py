#!/usr/bin/python3.10
"""Script for converting semantic sequential representation of music labels (produced by the model) to music21 stream
usable by music21 library to export to other formats.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import re
import music21 as music


def semantic_to_music21(labels: str) -> music.stream:
    """Converts labels to music21 format.

    Args:
        labels (str): one line of labels in semantic format without any prefixes.
    """
    labels_parsed = convert_line_to_groups(labels)
    print(labels_parsed)

    measures = []
    for measure in labels_parsed:
        for label_group in measure:
            if not label_group:
                continue

    DEFAULT_RETURN_VALUE = music.stream.Stream([music.note.Note('C4', type='half'),
                                                music.note.Note('D4', type='half'),
                                                music.note.Note('E')])
    return DEFAULT_RETURN_VALUE


def label_to_symbol(label: str) -> music.stream:
    """Converts one label to music21 format.

    Args:
        label (str): one symbol in semantic format as string
    """
    out = "UNKNOWN"

    return out


def convert_line_to_groups(labels: str) -> list:
    """Converts one line of labels in semantic format to a list of lists of lists. See example below.

    Args:
        labels (str): one line of labels in semantic format without any prefixes.

    Returns:
        list: list of lists of lists. Each list represents one measure. Each inner list represents one label group.
            Each inner-inner list represents labels in the group.

    Example with simplified labels:
        'C4 + D4 E4 + barline + G4 A4 + barline ' ->
        [
            [
                ['C4'],
                ['D4', 'E4']
            ],
            [
                ['G4', 'A4']
            ]
        ]
    """
    # remove parentheses if there
    labels = labels.strip('"')

    measures = re.split(r'\s\+\sbarline\s\+\s', labels)

    labels_parsed = []
    for measure in measures:
        label_groups = re.split(r'\s\+\s', measure.strip(''))

        measure_parsed = []
        for label_group in label_groups:
            label_group_parsed = re.split(r'\s', label_group)
            label_group_parsed = list(filter(None, label_group_parsed))
            measure_parsed.append(label_group_parsed)

            if measure_parsed[-1] == ['barline']:
                measure_parsed.pop()

        labels_parsed.append(measure_parsed)
    return labels_parsed
