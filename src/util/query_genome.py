import argparse
import os
import glob
import pickle
import seqgen
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
        file_handle.write(">query\n")
        file_handle.write(sequence + "\n")
    return "query.fa"


def bloom_gem_query(sequence, path):
    """
    Queries the bloom filters on the path
    :param sequence: the sequence to query
    :param path: the path to the bloom filters
    :return: a map with the potential sgrna sequence and it files it is likely to be in
    """
    potential_sequences = seqgen.generate_sequences(sequence)
    fa_files = glob.glob(path + os.path.sep + str("*.fa"))
    sequence_file_map = {}
    for fa_file in fa_files:
        count = 0
        bloom_file = fa_file + ".pkl"
        print "Opening " + bloom_file
        bloom_filter = pickle.load(open(bloom_file, 'rb'))
        for seq in potential_sequences:
            if seq in bloom_filter:
                count += 1
                if seq in sequence_file_map:
                    sequence_file_map[seq].append(str(fa_file))
                else:
                    sequence_file_map[seq] = [str(fa_file)]
        print "\t" + str(count) + " matches in this chromosome\n"
    return sequence_file_map


def main(get_cmd_line_args=True, input_args=None):
    """
    Main Sentinel.
    :return: None
    """
    args = parse_cmd_args() if get_cmd_line_args else input_args
    query_file = make_query_file(args["sequence"])
    print bloom_gem_query(args["sequence"], args["path"])

