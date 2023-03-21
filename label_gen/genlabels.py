"""
Script for parsing MusicXML and generating ground truth
sequence labels in desired manner. This version generates ground truth
sequence labels for the first line of the first part of the MusicXML file.
python genlabels.py -input <.musicxmls directory> -output <.semantic directory>
"""

import sys
import os
import argparse
import time
import re
# import logging

from musicxml import MusicXML


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
        '-o', '--output-folder', type=str, required=True,
        help='Path to the output directory to write sequences.')
    # parser.add_argument(
    #     '-v', "--verbose", action='store_true', default=False,
    #     help="Activate verbose logging.")
    return parser.parse_args()

def save_labels(output_file, labels_db) -> None:
    """Save labels form list of tuples to a file."""
    output_lines = [f'{file} "{labels}"' for file, labels in labels_db]
    new_lines_len = len(output_lines)

    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            orig_file = f.read()
            orig_lines = re.split('\n', orig_file)

            # filter out empty lines
            orig_lines = list(filter(None, orig_lines))

        output_lines = sorted(set(output_lines + orig_lines))
        print(f'Saving new {new_lines_len} label lines to original {len(orig_lines)}, '
              f'new total: {len(output_lines)}')

    output = '\n'.join(sorted(output_lines)) + '\n'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)


def get_files(folder):
    """Get list of existing files in folder with right file extension."""
    # listdir
    input_files = [f for f in os.listdir(folder)]

    # concat with input folder
    input_files = [os.path.join(folder, f) for f in input_files]

    # check existing files with correct extension '.musicxml'
    return [f for f in input_files if os.path.isfile(f) and f.endswith('.musicxml')]


def main():
    args = parseargs()

    start = time.time()

    labels_all = []
    input_files = get_files(args.input_folder)

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # Go through all inputs generating output sequences
    for _, file_name in enumerate(input_files):
        # Create a MusicXML object for generating sequences
        musicxml_obj = MusicXML(input_file=file_name)
        # musicxml_obj = MusicXML(input_file=input_path, output_file=output_path)

        # Generate output sequence
        # try:
        labels_all += musicxml_obj.write_sequences()
        # except UnicodeDecodeError: # Ignore bad MusicXML
        #     pass

    print('--------------------------------------')
    db_file_name = 'generated_labels.semantic'
    db_file_name_path = os.path.join(args.output_folder, db_file_name)
    save_labels(db_file_name_path, labels_all)
    print('Results:')
    print(f'From {len(input_files)} input files')
    print(f'\tgot {len(labels_all)} label lines')
    # for file, labels in labels_all:
    #     print(labels)

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == '__main__':
    main()
