import numpy as np
import skimage.io as io
from scipy import ndimage
import matplotlib.pyplot as plt
from skimage import measure
from skimage import morphology
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy.interpolate import CubicSpline
from skimage import filters
import scipy.misc


color_index = 0
color_list = [[255,0,0,255], [0,255,0,255], [0,0,255,255],
              [255, 255, 0, 255], [255, 0, 255, 255], [0, 255, 255, 255],
              [192, 192, 192, 255], [128, 0, 0, 255], [128, 128, 0, 255],
              [0, 128, 0, 255], [128, 0, 128, 255], [0, 128, 128, 255],
              [0, 0, 128, 255], [128, 128, 128, 255], [255, 69, 0, 255],
              [0, 100, 0, 255], [102, 205, 170, 255], [176, 224, 230, 255],
              [123, 104, 238, 255], [218, 112, 214, 255], [255, 182, 193, 255]]

color_map = {0:[0,0,0,255]}
debug_enabled = False

def getColorForNumber(forNumber):
    global color_map
    global color_index
    global color_list
    if (forNumber not in color_map):
        if (color_index >= len(color_list)):
            color_index = 0
        color_map[forNumber] = color_list[color_index]
        color_index += 1
    return color_map[forNumber]


def debugPlot(z_size, ar):
    global debug_enabled
    if (debug_enabled):
        plt.figure(figsize=(16, 16))
        for i in range(0, z_size):
            plt.subplot(5, 5, i + 1)
            plt.imshow(ar[i, ...])
        plt.show()

#Load the image
#image_stack = io.imread('resources/Full_LA_C6M1_A.tif')
image_stack = io.imread('resources/stack/stack0.tif')

z_size, x_size, y_size = image_stack.shape
z_scale = 1.00
xy_scale = 0.5
print 'Loaded image'

#Do a median filter
for i in range(0, z_size):
   image_stack[i] = ndimage.median_filter(image_stack[i, ...], 8)
   print "Finished working on 2d slice number : %d/%d" % (i+1, z_size)
medianImage = image_stack
print 'Done median filter'
imageFilter = filters.threshold_otsu(medianImage)
isolatedImage = medianImage < imageFilter

#Show what median filter did
debugPlot(z_size, isolatedImage)

#Do the cubic

#CubicSpline(x, y[, axis, bc_type, extrapolate])
isolatedImage = -isolatedImage
distance = ndimage.distance_transform_edt(isolatedImage)
print "Generated distance."
debugPlot(z_size, distance)
local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((20,20,20)), exclude_border=False, labels=isolatedImage)
debugPlot(z_size, local_maxi)
markers = morphology.label(local_maxi)

print 'Generated markers.'
labels_ws = watershed(-distance, markers, mask=isolatedImage)
debugPlot(z_size, labels_ws)

#for i in range(0, z_size):
#    plt.imshow(labels_ws[i, ...])
#    name = "stack%s.tif" % i
#    plt.savefig(name)

colorized = np.ndarray(shape=(z_size, x_size, y_size, 4), dtype=int)
for x in range(0, x_size):
    for y in range(0, y_size):
        for z in range(0, z_size):
            colorized[z][x][y] = getColorForNumber(labels_ws[z][x][y])

print 'Generated watershed.'
print 'Count: ' + str(len(np.unique(labels_ws))-1)
for i in range(0, z_size):
    name = "resources/stack/stack%s.tif" % i
    sliceofcolor = colorized[i, ...]
    scipy.misc.toimage(sliceofcolor).save(name)
#   #io.imsave(name, sliceofcolor)

