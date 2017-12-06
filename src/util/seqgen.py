import json
import os

ALPHA = 'ACGT'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

config = json.loads(open(DIR_PATH + '/../config.json').read())


def gc_content(seq):
    total = float(len(seq))
    gc = float(len([c for c in seq if c == 'G' or c == 'C']))

    return int((gc / total) * 100)


def crude_score_sequence(seq):
    gc_content_low = config['gc_content_threshold']['low']
    gc_content_high = config['gc_content_threshold']['high']

    gc = gc_content(seq[:20])

    if gc in range(gc_content_low, gc_content_high + 1):
        gc_score = 1
    else:
        gc_score = 0.5

    if seq[19] == 'G':
        g20_score = 1
    else:
        g20_score = 0.75

    if seq[19] == 'C':
        c20_minus_score = 0.75
    else:
        c20_minus_score = 1

    if seq[15] == 'C':
        c16_score = 1
    else:
        c16_score = 0.8

    if seq[15] == 'G':
        g16_minus_score = 0.8
    else:
        g16_minus_score = 1

    if seq[9] == 'A':
        a10_score = 1
    else:
        a10_score = 0.9

    # check PAM
    if seq[20] == 'C':
        pam_variable_score = 1
    elif seq[20] == 'T':
        pam_variable_score = 0.5
    else:
        pam_variable_score = 0.8

    return (gc_score * g20_score * c20_minus_score * c16_score * g16_minus_score * a10_score * pam_variable_score)


def generate_hamming_neighbors(st, alph, edits=1):
    ret = set()

    def __edit_neighbors_help(st, edits, leftmost_editable):

        for i in range(leftmost_editable, len(st)):
            if edits > 0:
                # Mismatch at position i
                for a in alph:
                    if a != st[i]:
                        newst = st[:i] + a + st[i + 1:]
                        __edit_neighbors_help(newst, edits - 1, i + 1)
        ret.add(st)

    __edit_neighbors_help(st, edits, 0)

    return ret


def generate_sequences(sgrna):
    sgrna = sgrna.upper()

    pam_sequences = config['pam_sequences']

    sequence_length = config['sequence_length']
    seed_sequence_length = config['seed_sequence_length']
    non_seed_sequence_length = (sequence_length - seed_sequence_length)

    seed_sequence = sgrna[non_seed_sequence_length:sequence_length]
    non_seed_sequence = sgrna[:non_seed_sequence_length]

    non_seed_neighbors = generate_hamming_neighbors(non_seed_sequence, ALPHA, config['mismatch_tolerance']['non_seed'])
    seed_neighbors = generate_hamming_neighbors(seed_sequence, ALPHA, config['mismatch_tolerance']['seed'])

    all_sequences = list(set(
        [non_seed + seed + pam for non_seed in non_seed_neighbors for seed in seed_neighbors for pam in pam_sequences]))
    print "Number of generated sequences " + str((len(all_sequences)))
    return all_sequences
