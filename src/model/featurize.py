import json
import itertools
import os
import csv


def generate_poly_nucleotides(alpha, max_n=4):
    poly_nucleotides = []
    for i in range(1, max_n + 1):
        poly_list = [alpha] * i
        expansions_arr = itertools.product(*poly_list)
        poly_nucleotides.append([''.join(e) for e in expansions_arr])

    return [item for sublist in poly_nucleotides for item in sublist]


def extract_positional_features(seq, nucleotide):
    positional_features = {}
    for pos in range(0, len(seq) - (len(nucleotide) - 1)):
        if seq[pos: pos + len(nucleotide)] == nucleotide:
            positional_features['{}_{}'.format(nucleotide, pos + 1)] = 1
        else:
            positional_features['{}_{}'.format(nucleotide, pos + 1)] = 0

    return positional_features


def mfe(seq):
    with open('in.csv', 'w') as in_file:
        in_file.write(seq)

    os.system('RNAfold < in.csv > out.csv')

    with open('out.csv') as out_file:
        mfe_output = out_file.read()

    output_stripped = mfe_output.split('\n')[1]
    output_stripped = output_stripped[len(seq) + 3:len(output_stripped) - 1]

    return float(output_stripped)


def heat(seq):
    with open('in.csv', 'w') as in_file:
        in_file.write(seq)

    os.system('RNAheat --Tmin=50 --Tmax=50 < in.csv > out.csv')

    with open('out.csv') as out_file:
        heat_output = out_file.read()

    os.system('rm in.csv out.csv')

    return float(heat_output.replace('\n', '').split('\t')[1])


def extract_features(processed_json):
    seq = processed_json['sequence']
    alpha = ['A', 'C', 'G', 'T']
    poly_nucleotides = generate_poly_nucleotides(alpha)
    features = {p: seq.count(p) for p in poly_nucleotides}

    for p in poly_nucleotides:
        features.update(extract_positional_features(seq, p))

    features.update(
        {'cut_position': processed_json['cut_position'], 'percent_peptide': processed_json['percent_peptide']})
    features.update({'mfe': mfe(seq), 'specific_heat': heat(seq)})
    features.update({'score': processed_json['score']})

    return features

processed_data = json.loads(open('src/model/data/processed.json').read())

featurized_data = []

for i, data in enumerate(processed_data):
    print('featurizing {}'.format(i))
    featurized_data.append(extract_features(data))

with open('src/model/data/featurized2.csv', 'wb') as csv_file:
    dict_writer = csv.DictWriter(csv_file, featurized_data[0].keys())
    dict_writer.writeheader()

    for i, data in enumerate(featurized_data):
        print('writing row {}'.format(i))
        dict_writer.writerow(data)
