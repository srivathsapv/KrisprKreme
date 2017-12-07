import argparse
import json
from util import build_index, validate, query_genome, consolidate_scores


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
    build_parser.set_defaults(which="build_parser")
    build_parser.add_argument('-p', '--path', type=str,
                              required=True,
                              help='path to the directory with all the fasta files.')

    # Query sub parser
    query_parser = subparsers.add_parser('query', help="options to query an sgRNA sequence in the genome")
    query_parser.set_defaults(which="query_parser")
    query_parser.add_argument('-p', '--path',
                              type=str,
                              required=True,
                              help="path to the directory with the bloom filter pickles and gems")
    query_parser.add_argument('-s', '--sequence', required=True, help="The query sequence")
    query_parser.add_argument("-o", "--output", type=str, required=True, help="Where to write the output file")

    # Score sub parser
    score_parser = subparsers.add_parser('score', help="options to query an sgRNA sequence in the genome")
    score_parser.set_defaults(which="score_parser")
    score_parser.add_argument('-i', '--input',
                              type=str,
                              required=True,
                              help="path to the input json file")
    score_parser.add_argument('-s', '--sequence', required=True, help="The query sequence")
    score_parser.add_argument("-o", "--output", type=str, required=True, help="Where to write the output file")

    # Parse args
    args = parser.parse_args()
    return vars(args)


def handle_build_parser(args):
    """Handles the build index portion of the program

    Passes the cmdline args to the build_index module

    Arguments:
        args {map} -- A dict with the cmdline arguments
    """
    build_index.main(False, args)


def handle_query_parser(args):
    """Handles the query portion of the program

    Passes the cmdline args to the genome_query module

    Arguments:
        args {map} -- A dict with the cmdline arguments
    """
    sgrna = args["sequence"]
    validate.is_valid_sgrna(sgrna)
    query_genome.main(False, args)


def handle_score_parser(args):
    """Handles the build score portion of the program

    Passes the cmdline args to the score module

    Arguments:
        args {map} -- A dict with the cmdline arguments
    """
    final_vals = consolidate_scores.rank_putative_sites(args["sequence"], args["input"])
    with open(args["output"], 'w') as file_handle:
        file_handle.write(json.dumps(final_vals, indent=4, sort_keys=True))


def main():
    """Main Sentinel

    Prevents the module from flywheeling if included
    """
    args = parse_cmd_args()
    globals()["handle_" + str(args["which"])](args)


if __name__ == "__main__":
    main()
