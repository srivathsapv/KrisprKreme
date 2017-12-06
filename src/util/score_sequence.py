import pickle
from featurize_helper import extract_features, get_data_with_important_features
import json

processed_data = json.loads(open('src/model/data/processed.json').read())

def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        return -1

    return len([i for i in xrange(len(str1)) if str1[i] != str2[i]])

def get_score(seq):
    hamming_dist = [(i, hamming_distance(seq, d['sequence'])) for i, d in enumerate(processed_data)]
    hamming_dist.sort(key=lambda tup:tup[1])

    nearest_sequence = processed_data[hamming_dist[0][0]]

    seq_json = {
        'cut_position': nearest_sequence['cut_position'],
        'percent_peptide': nearest_sequence['percent_peptide'],
        'sequence': seq
    }

    featurized_row = get_data_with_important_features(0.5, [extract_features(seq_json)], False)[0]
    dlist = [float(v) for k, v in featurized_row.iteritems() if k != 'score']
    model = pickle.load(open('src/model_files/rf_150_16.pkl', 'rb'))
    return model.predict([dlist])[0]
