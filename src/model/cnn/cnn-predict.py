import sys
import matplotlib.image as mp
import numpy as np
import png
sys.path.append('/Users/srivathsa/projects/caffe/python/')

import caffe
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

caffe.set_mode_cpu()
net = caffe.Net('sgrna-inception.prototxt', './data/_iter_5000.caffemodel', caffe.TEST)

img = mp.imread('./data/bit-images/seq_5282.png')

img_trans = np.ndarray((3, 30, 4))
img_trans[0, :, :] = np.transpose(img)
img_trans[1, :, :] = np.transpose(img)
img_trans[2, :, :] = np.transpose(img)

#print(img_trans)
net.forward()

# print(np.unique(net.blobs['conv2a_5x5'].data[0], return_counts=True))
# print(np.unique(net.blobs['conv2b_3x3'].data[0], return_counts=True))
# print(np.unique(net.blobs['maxpool2c'].data[0], return_counts=True))
neuron_image = net.blobs['conv2a_5x5'].data[27, 1]

x, y = neuron_image.shape

nw_peep = np.ndarray((x, y, 3))
nw_peep[:, :, 0] =  neuron_image
nw_peep[:, :, 1] =  neuron_image
nw_peep[:, :, 2] =  neuron_image

print(np.unique(neuron_image))
png.from_array(nw_peep.astype(np.uint8), 'RGB').save('nw_peep.png')

# out = net.forward()
# print(out)
