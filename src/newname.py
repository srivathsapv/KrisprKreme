import argparse
import os

FA_PATH = "$PWD/util/gemtools-1.7.1-i3/bin/chr22.fa"
GEM_PATH = "$PWD/util/gemtools-1.7.1-i3/bin/chr22"
GEM_GEM_PATH = "$PWD/util/gemtools-1.7.1-i3/bin/chr22.gem"
QUERY_PATH = "$PWD/util/gemtools-1.7.1-i3/bin/chr22q.fa"
INDEX_COMMAND = "gem-indexer -i " + FA_PATH + " -o " + GEM_PATH + " -c 'dna'"
MAP_COMMAND = "gem-mapper -I " + GEM_GEM_PATH + " -i " + QUERY_PATH + " -q 'ignore' -m 0 -o $PWD/util/gemtools-1.7.1-i3/bin/crispr"
SAM_PATH = "util/gemtools-1.7.1-i3/bin/crispr.sam"
SAM_COMMAND = "gem-2-sam -i $PWD/util/gemtools-1.7.1-i3/bin/crispr.map -o " + SAM_PATH


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='run the procedure of advice opinion extraction')
    parser.add_argument('-i', '--input', required=True, type=str, default=-1, help='a 23 nucleotide long input string')
    args = parser.parse_args()
    return args


def create_indices():
    # os.system(INDEX_COMMAND)
    os.system(MAP_COMMAND)
    os.system(SAM_COMMAND)


def parse_sam_file(infile):
    match_list = []
    with open(infile, 'r') as query:
        for line in query:
            line = line.rstrip()

            # Get each line delimited by tab
            if line.startswith('@'):
                continue
            else:
                line = line.split("\t")
                # Get the reference seq name from 3rd column, offset from 4th column and edit transcript  from the 6th column
                refseq_name = line[2]
                offset = line[3]
                edit_transcript = line[5]

                match_list.append(offset)

    return match_list


def main():
    args = parse_cmd_args()
    create_indices()
    matches = parse_sam_file(SAM_PATH)


if __name__ == "__main__":
    main()
