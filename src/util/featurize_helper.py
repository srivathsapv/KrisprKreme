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

    os.system('rm in.csv out.csv')

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


def extract_features(processed_json, score=None):
    seq = processed_json['sequence']
    alpha = ['A', 'C', 'G', 'T']
    poly_nucleotides = generate_poly_nucleotides(alpha)
    features = {p: seq.count(p) for p in poly_nucleotides}

    for p in poly_nucleotides:
        features.update(extract_positional_features(seq, p))

    features.update(
        {'cut_position': processed_json['cut_position'], 'percent_peptide': processed_json['percent_peptide']})
    features.update({'mfe': mfe(seq), 'specific_heat': heat(seq)})

    if not score:
        features.update({'score': processed_json['score']})

    return features


def get_data_with_important_features(score_threshold, featurized_data, score=True):
    importance_field_names = ('X', 'MeanDecreaseGini')
    reader = csv.DictReader(open('datasets/crisprpred/pone.0181943.s002.csv'))

    feature_importance = list(reader)

    for feature in feature_importance:
        feature['MeanDecreaseGini'] = float(feature['MeanDecreaseGini'])

    sorted_importance = sorted(feature_importance, key=lambda k: k[importance_field_names[1]])
    sorted_importance.reverse()

    important_features = [feature['X'] for feature in sorted_importance if
                          feature['MeanDecreaseGini'] >= score_threshold]

    if score:
        important_features.append('score')

    dlist = []
    for row in featurized_data:
        new_data = {}
        for feature in important_features:
            if feature in row:
                new_data[feature] = row[feature]
            else:
                new_data[feature] = 0
        dlist.append(new_data)

    return dlist
