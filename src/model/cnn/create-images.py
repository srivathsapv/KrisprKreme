import numpy as np
import json
import png

processed_data = json.loads(open('../data/processed.json', 'r').read())

char_map = {
    'A': [1, 0, 0, 0],
    'C': [0, 1, 0, 0],
    'G': [0, 0, 1, 0],
    'T': [0, 0, 0, 1]
}

SEQUENCE_LENGTH = 30
ALPHA_LENGTH = 4

id_to_classes = []

for row in processed_data:
    print('create image for sequence id={}'.format(row['id']))
    file_name = 'seq_{}.png'.format(row['id'])
    seq = row['sequence']
    feature_img = np.ndarray((ALPHA_LENGTH, SEQUENCE_LENGTH))

    trunc_score = int(row['score']*10)/float(10)
    class_label = int(float('%.1f' % trunc_score) * 10)
    id_to_classes.append([row['id'], class_label])

    for i, c in enumerate(seq):
        feature_img[:, i] = char_map[c]

    png.from_array((feature_img * 255).astype(np.uint8), 'L').save('data/bit-images/{}'.format(file_name))

class_file = open('data/img_classes.txt', 'w')

for class_label in id_to_classes:
    class_file.write('{},{}\n'.format(class_label[0], class_label[1]))
