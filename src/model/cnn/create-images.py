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

def create_4x30_images():
    id_to_classes = []

    for row in processed_data:
        print('create image for sequence id={}'.format(row['id']))
        file_name = 'seq_{}.png'.format(row['id'])
        seq = row['sequence']
        feature_img = np.ndarray((ALPHA_LENGTH, SEQUENCE_LENGTH))

        trunc_score = int(row['score']*10)/float(10)
        class_label = int(float('%.1f' % trunc_score) * 10)
        two_class_label = 1 if class_label >= 5 else 0

        id_to_classes.append([row['id'], two_class_label])

        for i, c in enumerate(seq):
            feature_img[:, i] = char_map[c]

        png.from_array((feature_img * 255).astype(np.uint8), 'L').save('data/bit-images/4x30/{}'.format(file_name))

    class_file = open('data/img_4x30_classes.txt', 'w')

    for class_label in id_to_classes:
        class_file.write('{},{}\n'.format(class_label[0], class_label[1]))

def create_11x11_images():
    id_to_classes = []

    for row in processed_data:
        print('create image for sequence id={}'.format(row['id']))
        file_name = 'seq_{}.png'.format(row['id'])
        seq = row['sequence']
        feature_img = np.ndarray((32, 32, 3))

        trunc_score = int(row['score']*10)/float(10)
        class_label = int(float('%.1f' % trunc_score) * 10)
        two_class_label = 1 if class_label >= 5 else 0

        full_file_name = 'data/bit-images/32x32/{}'.format(file_name)
        id_to_classes.append([full_file_name, two_class_label])

        feature_list = []
        for i, c in enumerate(seq):
            feature_list.extend(char_map[c])

        feature_list.extend([0] * 904)
        reshaped_features = np.reshape(feature_list, (32, 32)) * 255

        feature_img[:, :, 0] = reshaped_features
        feature_img[:, :, 1] = reshaped_features
        feature_img[:, :, 2] = reshaped_features

        png.from_array((feature_img).astype(np.uint8), 'RGB').save(full_file_name)

    train_class_file = open('data/img_32x32_train_classes.txt', 'w')
    test_class_file = open('data/img_32x32_test_classes.txt', 'w')

    for class_label in id_to_classes[:5000]:
        train_class_file.write('{} {}\n'.format(class_label[0], class_label[1]))

    for class_label in id_to_classes[5000:]:
        test_class_file.write('{} {}\n'.format(class_label[0], class_label[1]))

create_11x11_images()
