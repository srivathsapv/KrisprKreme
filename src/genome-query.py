import argparse
import os
import util.score_sequence

FA_PATH = "$PWD/util/gemtools-1.7.1-i3/bin/chr22.fa"
FA_LOCAL = "util/gemtools-1.7.1-i3/bin/chr22.fa"
GEM_PATH = "$PWD/util/gemtools-1.7.1-i3/bin/chr22"
GEM_GEM_PATH = "$PWD/util/gemtools-1.7.1-i3/bin/chr22.gem"
QUERY_PATH = "$PWD/util/gemtools-1.7.1-i3/bin/chr22q.fa"
QUERY_LOCAL = "util/gemtools-1.7.1-i3/bin/chr22q.fa"
INDEX_COMMAND = "gem-indexer -i " + FA_PATH + " -o " + GEM_PATH + " -c 'dna'"
MAP_COMMAND = "gem-mapper -I " + GEM_GEM_PATH + " -i " + QUERY_PATH + " -q 'ignore' -m 0 -o $PWD/util/gemtools-1.7.1-i3/bin/crispr"
SAM_PATH = "util/gemtools-1.7.1-i3/bin/crispr.sam"
SAM_COMMAND = "gem-2-sam -i $PWD/util/gemtools-1.7.1-i3/bin/crispr.map -o " + SAM_PATH
QUERY_TARGET_LINE = ">chr22q"


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='run the procedure of advice opinion extraction')
    parser.add_argument('-i', '--input', required=True, type=str, default=-1,
                        help='a 23 nucleotide long sgRNA with PAM')
    args = parser.parse_args()
    return vars(args)


def create_indices():
    # os.system(INDEX_COMMAND)
    os.popen(MAP_COMMAND).read()
    os.popen(SAM_COMMAND).read()


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


def read_genome(infile):
    with open(infile, 'r') as fh:
        lines = fh.readlines()
    genome = ""
    lines = lines[1:]
    for line in lines:
        genome += line.strip()
    return genome


def prepare_query(sample):
    with open(QUERY_LOCAL, 'w')  as fh:
        fh.write(QUERY_TARGET_LINE)
        fh.write("\n")
        fh.write(sample)
        fh.write("\n")


def get_sequences(genome, matches):
    genome = genome.strip()
    sequences = []
    for match in matches:
        match = int(match)
        match -= 1
        match -= 3
        sequences.append(genome[match:match + 30].upper())
    return sequences


def score_sequences(sequences, input_sequence):
    seq_scores = []
    for sequence in sequences:
        score = util.score_sequence.get_score(sequence)
        seq_scores.append((score, sequence))
    seq_scores = sorted(seq_scores)
    seq_scores.reverse()
    print "Input Sequence: " + input_sequence + "\n"
    print "Score: Target Sequence"
    for score_seqs in seq_scores:
        print "{}:{}".format(score_seqs[0], score_seqs[1])


def main():
    args = parse_cmd_args()
    prepare_query(args['input'])
    create_indices()
    matches = parse_sam_file(SAM_PATH)
    genome = read_genome(FA_LOCAL)
    sequences = get_sequences(genome, matches)
    score_sequences(sequences, args['input'])


if __name__ == "__main__":
    main()
