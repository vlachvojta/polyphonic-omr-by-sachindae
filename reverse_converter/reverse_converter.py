#!/usr/bin/python3.10
"""Script for converting sequential representation of music labels (produced by the model) to standard musicxml format
usable by external tools.

Gets list of input files where every file contains lines of semantic labels with corresponding IDs
in one of the following shapes:
    00005.jpg 000000 ">2 nb2..."
    00006.jpg ">2 nb2..."

Creates musicxml for every line and names it according to the ID at the beginning of each line.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import os
import sys
import time
import logging

import music21 as music
from semantic_to_music21 import semantic_line_to_music21_score
import common_rev_conv


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
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    ReverseConverter(
        input_files=args.input_files,
        output_folder=args.output_folder,
        verbose=args.verbose)()

    end = time.time()
    print(f'Total time: {end - start}')


class ReverseConverter:
    def __init__(self, input_files: list[str] = None, output_folder: str = 'output_musicxml', verbose: bool = False):
        self.output_folder = output_folder

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]  \t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)-s]\t- %(message)s')

        logging.debug('Hello World! (from ReverseConverter)')

        self.input_files = ReverseConverter.get_input_files(input_files)
        ReverseConverter.prepare_output_folder(output_folder)

    def __call__(self):
        if not self.input_files:
            logging.error('No input files provided. Exiting...')
            sys.exit(1)

        # For every file, convert it to MusicXML
        for input_file_name in self.input_files:
            logging.debug(f'Reading file {input_file_name}')
            lines = ReverseConverter.read_file_lines(input_file_name)

            for i, line in enumerate(lines):
                match = re.fullmatch(r'([a-zA-Z0-9_\-]+)[a-zA-Z0-9_\.]+\s+([0-9]+\s+)?\"([\S\s]+)\"', line)

                if not match:
                    logging.debug(f'NOT MATCHING PATTERN. Skipping line {i} in file {input_file_name}: '
                                  f'({line[:min(50, len(line))]}...)')
                    continue

                stave_id = match.group(1)
                labels = match.group(3)
                output_file_name = os.path.join(self.output_folder, f'{stave_id}.musicxml')

                parsed_labels = semantic_line_to_music21_score(labels)
                if not isinstance(parsed_labels, music.stream.Stream):
                    logging.error(f'Labels could not be parsed. Skipping line {i} in file {input_file_name}: '
                                  f'({line[:min(50, len(line))]}...)')
                    continue

                logging.info(f'Parsing successfully completed.')
                # parsed_labels.show()  # Show parsed labels in some visual program (MuseScore by default)

                xml = common_rev_conv.music21_to_musicxml(parsed_labels)
                common_rev_conv.write_to_file(output_file_name, xml)

    @staticmethod
    def prepare_output_folder(output_folder: str):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    @staticmethod
    def get_input_files(input_files: list[str] = None):
        existing_files = []

        if not input_files:
            return []

        for input_file in input_files:
            if os.path.isfile(input_file):
                existing_files.append(input_file)

        return existing_files

    @staticmethod
    def read_file_lines(input_file: str) -> list[str]:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        if not lines:
            logging.warning(f'File {input_file} is empty!')

        return [line for line in lines if line]


if __name__ == '__main__':
    main()
