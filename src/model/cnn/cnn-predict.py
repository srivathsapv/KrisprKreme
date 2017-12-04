import sys
import matplotlib.image as mp
import numpy as np
sys.path.append('/Users/srivathsa/projects/caffe/python/')

import caffe
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

caffe.set_mode_cpu()
net = caffe.Net('sgrna-simple-deploy.prototxt', './data/_iter_10000.caffemodel', caffe.TEST)

img = mp.imread('./data/bit-images/seq_5282.png')

img_trans = np.ndarray((3, 30, 4))
img_trans[0, :, :] = np.transpose(img)
img_trans[1, :, :] = np.transpose(img)
img_trans[2, :, :] = np.transpose(img)

#print(img_trans)

net.blobs['data'].data[...] = img_trans

out = net.forward()
print(out['prob'])
