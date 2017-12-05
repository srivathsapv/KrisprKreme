"""
Driver Script
"""
import argparse

def parse_cmd_args():
    """Parses Command Line args

    Expects the user to provide command line arguments

    Returns:
        map -- a map of command line argument names to values
    """

    parser = argparse.ArgumentParser(description='A tool for crispr analysis')
    subparsers = parser.add_subparsers()

    # Build sub parser
    build_parser = subparsers.add_parser('build', help="options to build the bloom filter indices")
    build_parser.add_argument('-p', '--path', type=str,
                              required=True,
                              help='path to the directory with all the fasta files.')

    # Query sub parser
    query_parser = subparsers.add_parser('query', help="options to query an sgRNA sequence in the genome")
    query_parser.add_argument('-p', '--path',
                              type=str,
                              required=True,
                              help="path to the directory with the bloom filter pickles")
    query_parser.add_argument('-s', '--sequence', required=True, help="The query sequence")
    query_parser.add_argument("-o", "--ouput", type=str, required=True, help="Where to write the output file")

    # Parse args
    args = parser.parse_args()
    return vars(args)


def main():
    """Main Sentinel

    Prevents the module from flywheeling if included
    """
    parse_cmd_args()

if __name__ == "__main__":
    main()
