"""
Script for parsing MusicXML and generating ground truth
sequence labels in desired manner. This version generates ground truth
sequence labels for the first line of the first part of the MusicXML file.
python genlabels.py -input <.musicxmls directory> -output <.semantic directory>
"""

import sys
import os
import argparse
# import logging

from musicxml import MusicXML


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-folder', dest='input', type=str,   # required='-c' not in sys.argv,
        help='Path to the input directory with MusicXMLs.')
    parser.add_argument(
        '-o', '-output-folder', dest='output', type=str, required=True,
        help='Path to the output directory to write sequences.')
    # parser.add_argument(
    #     '-v', "--verbose", action='store_true', default=False,
    #     help="Activate verbose logging.")
    return parser.parse_args()


def main():
    args = parseargs()

    #print('Input dir (MusicXMLs):', args.input)
    #print('Output dir (Sequences):', args.output)

    # if args.verbose:
    #     logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
    # else:
    #     logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

    # For tracking number of MusicXML files read
    file_num = 0

    # Go through all inputs generating output sequences
    for i, file_name in enumerate(os.listdir(args.input)):

        # Ignore non .musicxml files
        if not file_name.endswith('.musicxml'):
            continue

        if not os.path.exists(args.output):
            os.makedirs(args.output)

        # Create a MusicXML object for generating sequences
        input_path = os.path.join(args.input, file_name)
        output_path = os.path.join(args.output, ''.join(file_name.split('.')[:-1]))
        musicxml_obj = MusicXML(input_file=input_path, output_file=output_path)

        # Generate output sequence
        try:
            musicxml_obj.write_sequences()
            file_num += 1
        except UnicodeDecodeError: # Ignore bad MusicXML
            pass

    print('Num MusicXML files read:', file_num)


if __name__ == '__main__':
    main()