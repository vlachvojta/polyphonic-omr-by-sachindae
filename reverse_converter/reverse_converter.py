#!/usr/bin/python3.8
"""Script for converting sequential representation of music labels (produced by the model) to standard musicxml format
usable by external tools.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz

TODO: write docu after development

Modes:  ??? TODO: decide which mode to implement
    - 1to1 (1 label-sequence => 1 XML file)
    - Nto1 (group of label-sequences with same ID prefix => 1 XML file)
"""

import argparse
import re
import os
import sys
import time
import logging


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------\n')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-files', nargs='*', default=[],  # required='-c' not in sys.argv,
        help='Path to the input file with sequences as lines.')
    parser.add_argument(
        '-o', '--output-folder', type=str, default='output_musicxml',
        help='Path to the output directory to write MusicXMLs.')
    # parser.add_argument(
    #     '-m', '--mode', type=str, default='new-system', choices=['orig', 'new-system'],
    #     help=('Set mode of separating labels to systems. Original takes note widths, '
    #           'new-system looks for new-system and new-page tags.'))
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    print(type(args.input_files))
    print(args.input_files)

    start = time.time()
    ReverseConverter(
        input_files=args.input_files,
        output_folder=args.output_folder,
        verbose=args.verbose)()

    end = time.time()
    print(f'Total time: {end - start}')


def prepare_output_folder(output_folder: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


def get_input_files(input_files: list[str] = None):
    existing_files = []

    if not input_files:
        return []

    for input_file in input_files:
        if os.path.isfile(input_file):
            existing_files.append(input_file)

    return existing_files


def read_file_lines(input_file: str) -> list[str]:
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    if not lines:
        logging.warning(f'File {input_file} is empty!')

    return [line for line in lines if line]


class ReverseConverter:
    def __init__(self, input_files: list[str] = None, output_folder: str = 'output_musicxml', verbose: bool = False):
        self.output_folder = output_folder

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]  \t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)-s]\t- %(message)s')

        logging.debug('Hello World! (from ReverseConverter)')

        self.input_files = get_input_files(input_files)
        prepare_output_folder(output_folder)

    def __call__(self):
        # For every file, convert it to MusicXML
        for input_file_name in self.input_files:
            logging.debug(f'Reading file {input_file_name}')
            lines = read_file_lines(input_file_name)

            for i, line in enumerate(lines):
                match = re.fullmatch(r'([a-zA-Z0-9_]+) [0-9]+ \"([\S\s]+)\"', line)

                if not match:
                    logging.debug(f'NOT MATCHING PATTERN. Skipping line {i} in file {input_file_name}: '
                                  f'({line[:min(50, len(line))]}...)')
                    continue

                stave_id = match.group(1)
                labels = match.group(2)

                parsed_labels = self.convert_labels(labels)

                output_file_name = os.path.join(self.output_folder, f'{stave_id}.xml')

                # TODO: write tree to file output_file_name / use music21 native musicxml export

    def convert_labels(self, labels):
        measures = re.split(r'|', labels)

        # TODO: parse labels using music21 library which also supports export to musicxml


if __name__ == '__main__':
    main()
