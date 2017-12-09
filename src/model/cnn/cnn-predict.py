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
net = caffe.Net('sgrna-dcnn.prototxt', 'alpha_iter_10000.caffemodel', caffe.TEST)

img = mp.imread('./data/bit-images/32x32/seq_5282.png')
net.blobs['data'].reshape(*img.shape)
net.blobs['data'].data[...] = img

net.forward()
net_img = net.blobs['conv2'].data[0, :][0] * 255


x, y = net_img.shape
net_img_rgb = np.ndarray((x, y, 3))

net_img_rgb[:, :, 0] = net_img
net_img_rgb[:, :, 1] = net_img
net_img_rgb[:, :, 2] = net_img

png.from_array(net_img_rgb.astype(np.uint8), 'RGB').save('nw_peep.png')
