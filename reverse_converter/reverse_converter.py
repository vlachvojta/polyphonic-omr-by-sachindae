#!/usr/bin/python3.8
"""Script for converting sequential representation of music labels (produced by the model) to standard musicxml format
usable by external tools.

TODO: write docu after development

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import argparse
import re
import sys
import time
import logging


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-folder', type=str,   # required='-c' not in sys.argv,
        help='Path to the input directory with MusicXMLs.')
    parser.add_argument(
        '-o', '--output-folder', type=str, # required=True,
        help='Path to the output directory to write sequences.')
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

    start = time.time()
    ReverseConverter(
        input_file=args.input_folder,
        output_file=args.output_folder)

    end = time.time()
    print(f'Total time: {end - start}')


class ReverseConverter:
    def __init__(self, input_file, output_file, verbose: bool = False):
        self.input_file = input_file
        self.output_file = output_file

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)-s]\t- %(message)s')

        logging.debug('Hello World! (from ReverseConverter)')


if __name__ == '__main__':
    main()
