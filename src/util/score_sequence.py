import pickle
from featurize_helper import extract_features, get_data_with_important_features

def get_score(seq):
    seq_json = {
        'cut_position': 79,
        'percent_peptide': 36.24,
        'sequence': seq
    }

    featurized_row = get_data_with_important_features(0.5, [extract_features(seq_json)], False)[0]
    dlist = [float(v) for k, v in featurized_row.iteritems() if k != 'score']
    model = pickle.load(open('../model_files/rf_303_16.pkl', 'rb'))
    return model.predict([dlist])[0]
