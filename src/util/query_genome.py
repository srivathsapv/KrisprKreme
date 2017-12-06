import argparse
import os
import glob
import pickle

from pybloom import ScalableBloomFilter


def parse_cmd_args():
    """
    Parses command line args
    :return: A map of the args
    """
    parser = argparse.ArgumentParser(description='run the procedure of advice opinion extraction')
    parser.add_argument('-p', '--path',
                        type=str,
                        required=True,
                        help="path to the directory with the bloom filter pickles and gems")
    parser.add_argument('-s', '--sequence', required=True, help="The query sequence")
    parser.add_argument("-o", "--output", type=str, required=True, help="Where to write the output file")
    args = parser.parse_args()
    return vars(args)


def make_query_file(sequence):
    """
    Makes a query fasta file
    :param sequence: the query sequence
    :return: Path to created query file
    """
    with open("query.fa", "w") as file_handle:
        file_handle.write(">query")
        file_handle.write(sequence)
    return "query.fa"


def bloom_query(sequence, path):
    """
    Queries the bloom filters on the path
    :param sequence: the sequence to query
    :param path: the path to the bloom filters
    :return: a list of fasta files where the bloom filters are
    """
    fa_files = glob.glob(path + os.path.sep + str("*.fa"))
    matching_fas_files = []
    for fa_file in fa_files:
        bloom_file = fa_file + ".pkl"
        bloom_filter = pickle.load(open(bloom_file, 'rb'))
        if sequence in b


def main(get_cmd_line_args=True, input_args=None):
    """
    Main Sentinel.
    :return: None
    """
    args = parse_cmd_args() if get_cmd_line_args else input_args
    query_file = make_query_file(args["sequence"])
