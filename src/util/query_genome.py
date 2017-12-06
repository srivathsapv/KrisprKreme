"""
Author: Srinivas Suresh Kumar
Date: 12/5/2017
"""
import argparse
import os
import glob
import json
import pickle
import sys
import seqgen
import uuid

from colorama import init, Fore, Back, Style
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


def read_genome(infile):
    """
    Reads a fas file
    :param infile: 
    :return: 
    """
    with open(infile, 'r') as fh:
        lines = fh.readlines()
    genome = ""
    lines = lines[1:]
    for line in lines:
        genome += line.strip()
    return genome


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


def bloom_query(sequence, path):
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
        sys.stdout.write(" ")
        print (Fore.WHITE + Back.BLUE + "Opening " + bloom_file)
        bloom_filter = pickle.load(open(bloom_file, 'rb'))
        for seq in potential_sequences:
            if seq in bloom_filter:
                count += 1
                if seq in sequence_file_map:
                    sequence_file_map[seq].append(str(fa_file))
                else:
                    sequence_file_map[seq] = [str(fa_file)]
        print Style.RESET_ALL + "\t" + str(count) + " matches in this chromosome"
        print Style.RESET_ALL
    return sequence_file_map


def parse_sam_file(infile):
    # From shubha's sam parser
    match_list = []
    with open(infile, 'r') as query:
        for line in query:
            line = line.rstrip()

            # Get each line delimited by tab
            if line.startswith('@'):
                continue
            else:
                line = line.split("\t")
                offset = line[3]
                match_list.append(offset)

    return match_list


def gem_query(sequence_file_map):
    """
    Performs a gem query for every sequence and file in the sequence file map
    :param sequence_file_map: a map of sequences to fa files they occur in  
    :return: None
    """
    sys.stdout.write(Fore.WHITE + Back.RED + "\n Starting GEM query")
    sys.stdout.flush()
    alignment_list = []
    for seq in sequence_file_map:
        alignment_map = {}
        query_file = make_query_file(seq)
        for target_file in sequence_file_map[seq]:
            sys.stdout.write(".")
            sys.stdout.flush()
            alignment_map["id"] = str(uuid.uuid4())
            alignment_map["chr_path"] = str(target_file)
            alignment_map["query_sequqnce"] = seq
            gem_file = str(target_file) + ".gem"
            os.system(
                "gem-mapper -I " + gem_file + " -i " + query_file + " -q \'ignore\' -m 0 -o output >/dev/null 2>&1")
            os.system("gem-2-sam -i output.map -o output.sam >/dev/null 2>&1")
            matches = parse_sam_file("output.sam")
            for match in matches:
                match = int(match)
                match -= 5
                alignment_map["start"] = match
                alignment_map["end"] = int(match) + 30
                genome = read_genome(target_file)
                alignment_map["sequence"] = genome[match: (match + 30)]
                alignment_list.append(alignment_map)
    print "\n Done"
    return alignment_list


def query(sequence, path):
    """
    Performs a bloom filter query followed by a gem query
    :param sequence: the query sequence
    :param path: the path wo where the bloom filters, fa files and gem files are
    :return: an offset map
    """
    sequence_file_map = bloom_query(sequence, path)
    return gem_query(sequence_file_map)


def main(get_cmd_line_args=True, input_args=None):
    """
    Main Sentinel.
    :return: None
    """
    init()
    args = parse_cmd_args() if get_cmd_line_args else input_args
    # query_file = make_query_file(args["sequence"])
    answers = query(args["sequence"], args["path"])
    with open(args["output"], 'w') as output_file:
        output_file.write(json.dumps(answers))
