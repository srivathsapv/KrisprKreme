import sys
sys.path.append('/Users/srivathsa/projects/caffe/python/')

import caffe
import lmdb
import numpy as np
from caffe.io import array_to_datum
import matplotlib.image as mp

SEQUENCE_LENGTH = 30
ALPHA_LENGTH = 4

all_labels = []

for c in open('./data/img_classes.txt', 'r').read().split('\n'):
    if len(c.split(',')) < 2:
        continue
    all_labels.append(int(c.split(',')[1]))

IMG_BASE_NAME = './data/bit-images/seq_{}.png'

def create_lmdb(db_name, labels):
    map_size = SEQUENCE_LENGTH * ALPHA_LENGTH * 27 * len(labels) # 27x is just for safety
    env = lmdb.Environment(db_name, map_size=map_size)
    txn = env.begin(write=True, buffers=True)

    X_copy = np.ndarray((3, SEQUENCE_LENGTH, ALPHA_LENGTH))

    for i,label in enumerate(labels):
        print('writing img-{}'.format(i))
        X = mp.imread(IMG_BASE_NAME.format(i)) * 255
        X_rev = np.transpose(X)
        X_copy[0, :, :] = X_rev
        X_copy[1, :, :] = X_rev
        X_copy[2, :, :] = X_rev

        if label < 5:
            class_label = 0
        else:
            class_label = 1

        datum = array_to_datum(X_copy.astype(np.uint8), class_label)
        str_id = '{:08}'.format(i)
        txn.put(str_id.encode('ascii'), datum.SerializeToString())

    txn.commit()
    env.close()
    print('Done creating {}!'.format(db_name))

create_lmdb('sgrna_train_lmdb_dummy', all_labels[:5000])
create_lmdb('sgrna_test_lmdb', all_labels[5000:])
