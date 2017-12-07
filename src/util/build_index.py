
import argparse
import glob
import os
import pickle

from pybloom import ScalableBloomFilter

KMER_SIZE = 23
INPUT_SEQUENCE = ['X'] * 23
BLOOM_EXTENSION = ".pkl"


def parse_cmd_args():
    """
    Parses command line args.

    :return: A dictionary of command line arguments
    """
    parser = argparse.ArgumentParser(description='run the procedure of advice opinion extraction')
    parser.add_argument('-p', '--path', type=str, required=True, help='Path to the directory with all the fasta files.')
    args = parser.parse_args()
    return vars(args)


def get_file_list(path):
    """
    Gets the names of all the fasta files in the path.

    :param path: the path to the fasta files
    :return: The list of fasta files in the path with the path prefixed
    """
    return glob.glob(path + os.path.sep + str("*.fa"))


def save_object(obj, filename):
    """
    Saves an object as a pickle.

    :param obj: The object to persist
    :param filename: the name of the file to persist
    """
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def build_index(file_handle, file_name):
    """
    Build the bloom filter for a given fa file

    :param file_handle: The handle to the file
    :param file_name: The name of the file
    """
    c = True
    sbf = ScalableBloomFilter(mode=ScalableBloomFilter.LARGE_SET_GROWTH)
    while c:
        c = file_handle.read(1)
        if c != '\n':
            INPUT_SEQUENCE.pop(0)
            INPUT_SEQUENCE.append(c.upper())
            sequence = ''.join(INPUT_SEQUENCE)
            print "Processing: " + sequence
            sbf.add(sequence)
    save_object(sbf, str(file_name) + BLOOM_EXTENSION)
    os.system("gem-indexer -i " + file_name + " -o " + file_name + " -c \'dna\'")


def build_indices(files):
    """
    Build the bloom filter indices.

    :param files: the list of files for which the indices need to be built
    """
    for fa_file in files:
        with open(fa_file, "r") as file_handle:
            print fa_file
            file_handle.readline()  # read the first line
            build_index(file_handle, fa_file)
            print "\n done with file " + str(file_handle)


def main(get_command_line_args=True, cmdargs=None):
    """
    Main Sentinel.
    """
    args = parse_cmd_args() if get_command_line_args else cmdargs
    files = get_file_list(args["path"])
    build_indices(files)


if __name__ == "__main__":
    main()
