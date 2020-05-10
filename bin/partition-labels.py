#!/usr/bin/env python2
import argparse

from ingredient_phrase_tagger.training import labelled_data
from ingredient_phrase_tagger.training import partitioner


def main(args):
    with open(args.label_path) as label_file, open(
            args.training_path, 'wb') as training_file, open(
                args.testing_path, 'wb') as testing_file:
        label_reader = labelled_data.Reader(label_file)
        training_writer = labelled_data.Writer(training_file)
        testing_writer = labelled_data.Writer(testing_file)

        partitioner.split_labels(label_reader, training_writer, testing_writer,
                                 args.training_fraction, args.max_labels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ingredient-phrase-tagger: Label Partitioner',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--label-path',
        help='Path to input CSV of labelled ingredients',
        required=True)
    parser.add_argument(
        '--training-path',
        help='Path to output path to write training data',
        required=True)
    parser.add_argument(
        '--testing-path',
        help='Path to output path to write testing data',
        required=True)
    parser.add_argument(
        '--training-fraction',
        type=float,
        default=0.9,
        help=('Percentage of label set to use for training (remainder is '
              'reserved for testing)'))
    parser.add_argument(
        '--max-labels',
        help='Maximum number of labels to read from label-path',
        default=0,
        type=int)
    main(parser.parse_args())
