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
import os
import re
import time
import logging

import music21 as music

from semantic_to_music21 import parse_semantic_to_measures, encode_measures, Measure
from pero_ocr.core.layout import PageLayout, RegionLayout, TextLine
import common_rev_conv


def parseargs():
    print(' '.join(sys.argv))
    print('----------------------------------------------------------------------')
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input-xml-path", required=True, type=str,
        help="Path to input XML file with exported PageLayout.")
    parser.add_argument(
        "-t", "--translator-path", type=str, required=True,
        help="JSON File containing translation dictionary from shorter encoding (exported by model) to longest.")
    parser.add_argument(
        "-o", "--output-folder", default='output_page',
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
        translator_path=args.translator_path,
        output_folder=args.output_folder,
        verbose=args.verbose)()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


class PageLayoutToPage:
    """Take pageLayout XML exported from pero-ocr with transcriptions and re-construct page of musical notation."""

    def __init__(self, input_xml_path: str, translator_path: str,
                 output_folder: str, verbose: bool = False):
        self.translator_path = translator_path
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
        page = PageLayout(file=self.input_xml_path)
        print(f'Page {self.input_xml_path} loaded successfully.')
        translator = Translator(file_name=self.translator_path)

        parts = PageLayoutToPage.regions_to_parts(page.regions, translator)
        music_parts = []
        for part in parts:
            music_parts.append(part.encode_to_music21())

        # Finalize score creation
        metadata = music.metadata.Metadata()
        metadata.title = metadata.composer = ''
        score = music.stream.Score([metadata] + music_parts)

        # Export score to MusicXML or something
        output_file = self.get_output_file('musicxml')
        xml = common_rev_conv.music21_to_musicxml(score)
        common_rev_conv.write_to_file(output_file, xml)

    def get_output_file(self, extension: str = 'musicxml') -> str:
        input_file = os.path.basename(self.input_xml_path)
        name, *_ = re.split(r'\.', input_file)
        return os.path.join(self.output_folder, f'{name}.{extension}')

    @staticmethod
    def regions_to_parts(regions: list[RegionLayout], translator) -> list:  # -> list[Part]:
        """Takes a list of regions and splits them to parts."""
        max_parts = max([len(region.lines) for region in regions])
        print(f'Max parts: {max_parts}')

        # TODO add empty measure padding to parts without textlines

        parts = [Part(translator) for _ in range(max_parts)]
        for region in regions:
            for part, line in zip(parts, region.lines):
                part.add_textline(line)

        return parts


class Part:
    """Represent musical part (part of notation for one instrument/section)"""

    def __init__(self, translator):
        self.repr_music21 = music.stream.Part([music.instrument.Piano()])
        self.labels: list[str] = []
        self.measures: list[Measure] = []  # List of measures in internal representation, NOT music21
        self.translator = translator

    def add_textline(self, line: TextLine) -> None:
        labels = self.translator.convert_line(line.transcription, False)
        self.labels.append(labels)

        new_measures = parse_semantic_to_measures(labels)

        # Delete first clef symbol of first measure if same as previous
        if len(self.measures) and new_measures[0].get_start_clef() == self.measures[-1].last_clef:
            new_measures[0].delete_clef_symbol()

        new_measures_encoded = encode_measures(new_measures, len(self.measures) + 1)

        self.measures += new_measures
        self.repr_music21.append(new_measures_encoded)
        # print('--------------------------------')
        # print(labels)
        # self.repr_music21.show('text')

    def encode_to_music21(self) -> music.stream.Part:
        if self.repr_music21 is None:
            logging.info('Part empty')

        return self.repr_music21


class Translator:
    """Translator class for translating shorter SSemantic encoding to Semantic encoding using translator dictionary."""
    def __init__(self, file_name: str):
        self.translator = common_rev_conv.read_json(file_name)
        self.translator_reversed = {v: k for k, v in self.translator.items()}
        self.n_existing_labels = set()

    def convert_line(self, line, to_shorter: bool = True):
        line = line.strip('"').strip()
        symbols = re.split(r'\s+', line)
        converted_symbols = [self.convert_symbol(symbol, to_shorter) for symbol in symbols]

        return ' '.join(converted_symbols)

    def convert_symbol(self, symbol: str, to_shorter: bool = True):
        dictionary = self.translator if to_shorter else self.translator_reversed

        try:
            return dictionary[symbol]
        except KeyError:
            if symbol not in self.n_existing_labels:
                self.n_existing_labels.add(symbol)
                print(f'Not existing label: ({symbol})')
            return ''


if __name__ == "__main__":
    main()
