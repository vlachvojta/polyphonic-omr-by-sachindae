#!/usr/bin/python3.10
"""Script for testing every possible label in current semantic translator.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import os
import sys
import json
from semantic_to_music21 import label_to_stream


TRANSLATOR_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
    'bp-git', 'translators', 'translator.Semantic_to_SSemantic.json')


def main():
    translator = read_json_file(TRANSLATOR_FILE_PATH)
    semantic_symbols = list(translator.keys())

    unknown_outputs = []

    for symbol in semantic_symbols:
        output = label_to_stream(symbol)
        if output == 'UNKNOWN':
            unknown_outputs.append(symbol)

    print(f'Unknown outputs: {unknown_outputs}')
    print('================================================================')
    print('')
    print(f'Unknown outputs count: {len(unknown_outputs)}')


def read_json_file(file: str):
    """Read file, if file extension == 'json', read as json"""
    if not os.path.exists(file):
        return {}

    with open(file) as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    main()