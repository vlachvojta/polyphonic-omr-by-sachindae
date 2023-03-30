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
    parser.add_argument(
        '-m', '--mode', type=str, default='new-system', choices=['orig', 'new-system'],
        help=('Set mode of separating labels to systems. Original takes note widths, '
              'new-system looks for new-system and new-page tags.'))
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    return parser.parse_args()

# def label_db_list_to_dict(list_: list) -> dict:
#     """Go through a list of lines, separate the ID at the beginning and return as dictionary.
    
#     key:  sequence ID
#     value: sequence str"""
#     list_of_tuples = []
#     for item in list_:
#         splitted = re.split(r'\s', item)

#     output = {}
#     for (k, v) in list_:
#         output[k] = v
#     return output


# def update_labels(orig_labels: list, new_labels: list) -> list:
#     ...


def save_labels(output_file: str, labels_db: dict) -> None:
    """Save labels from dictionary to a file."""

    output_lines = [f'{file} "{labels}"' for file, labels in labels_db]
    # new_lines_len = len(output_lines)

    while True:
        if not os.path.exists(output_file):
            break
        split = re.split(r'\.', output_file)
        out_file_name_and_path = '.'.join(split[:-1])
        out_file_ext = split[-1]
        output_file = f'{out_file_name_and_path}_new.{out_file_ext}'

        # with open(output_file, 'r', encoding='utf-8') as f:
        #     orig_file = f.read()
        #     orig_lines = re.split('\n', orig_file)
        #     orig_lines_dict = 

        #     # filter out empty lines
        #     orig_lines = list(filter(None, orig_lines))

        # output_lines = sorted(set(output_lines + orig_lines))
        # print(f'Saving new {new_lines_len} label lines to original {len(orig_lines)}, '
        #       f'new total: {len(output_lines)}')

    output = '\n'.join(sorted(output_lines)) + '\n'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)


def get_files(folder):
    """Get list of existing files in folder with right file extension."""
    # listdir
    input_files = os.listdir(folder) if os.path.isdir(folder) else []

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

    if args.verbose:
        print(f'Found {len(input_files)} input files, generating labels. ')
    else:
        print(f'Found {len(input_files)} input files, generating labels. '
              '(every dot is 200 files, every line is 10_000)')

    # Go through all inputs generating output sequences
    for i, file_name in enumerate(input_files):
        if not args.verbose and i % 200 == 0 and i > 0:
            print('.', end='')
            if i % 10_000 == 0:
                print('')
            sys.stdout.flush()
        # Create a MusicXML object for generating sequences
        musicxml_obj = MusicXML(input_file=file_name, verbose=args.verbose, mode=args.mode)
        # musicxml_obj = MusicXML(input_file=input_path, output_file=output_path)

        # Generate output sequence
        labels_all += musicxml_obj.write_sequences()

    print('')
    print('--------------------------------------')
    db_file_name = 'labels.semantic'
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
