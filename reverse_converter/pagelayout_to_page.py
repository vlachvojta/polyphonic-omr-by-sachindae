#!/usr/bin/env python3.8
"""Script to take pageLayout XML from pero-ocr with transcriptions and re-construct page of musical notation.

What is the output? (options for future development)
 - music21 representation of page (this is first step)
 - pdf of a music notation
 - midi file?

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import sys
import argparse
import re
import os
import time
import lmdb
import logging

from pero_ocr.core.layout import PageLayout


def parseargs():
    print(' '.join(sys.argv))
    print('----------------------------------------------------------------------')
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input-xml-path", required=True, type=str,
        help="Path to input XML file with exported PageLayout.")
    parser.add_argument(
        "-o", "--output-folder", default='output_folder',
        help="Set output file with extension. Output format is JSON")
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")

    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()
    PageLayoutToPage(
        input_xml_path=args.input_xml_path,
        output_folder=args.output_folder,
        verbose=args.verbose)()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


class PageLayoutToPage:
    """Take pageLayout XML exported from pero-ocr with transcriptions and re-construct page of musical notation."""

    def __init__(self, input_xml_path: str, output_folder: str, verbose: bool = False):
        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]  \t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)-s]\t- %(message)s')

        if not os.path.isfile(input_xml_path):
            logging.error('No input file of this path was found')
        self.input_xml_path = input_xml_path

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.output_folder = output_folder

    def __call__(self) -> None:
        ...
        # Load XML
        # Iterate through regions and lines
        # Convert every line to a stream of music21
        # Concat lines to parts
        # Concat parts to score
        # Export


if __name__ == "__main__":
    main()
