import json

raw_data = json.loads(open('./data/raw.json').read())

new_list = []

for i, data in enumerate(raw_data):
    new_dict = {}
    new_dict['id'] = i
    new_dict['sequence'] = data['30mer']
    new_dict['cut_position'] = data['Amino Acid Cut position']
    new_dict['percent_peptide'] = data['Percent Peptide']
    new_dict['score'] = data['predictions']

    new_list.append(new_dict)

with open('./data/processed.json', 'w') as fp:
    json.dump(new_list, fp)
