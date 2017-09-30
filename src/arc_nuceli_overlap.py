import skimage.io as io
import numpy as np
from scipy import ndimage
from skimage import filters
from skimage.morphology import closing
from skimage import exposure
import sys
import time

class Overlap:

    __nuc_x_size = -1
    __nuc_y_size = -1
    __nuc_z_size = -1

    __arc_x_size = -1
    __arc_y_size = -1
    __arc_z_size = -1

    __segmented_nuclei = None
    __arc_signal = None
    __overlap_stack = None


    def __init__(self, segmented_image_stack, arc_segmented_stack):
        self.__segmented_nuclei = semgmented_image_stack
        self.__arc_signal = arc_segmented_stack
        self.__nuc_z_size, self.__nuc_x_size, self.__nuc_y_size = self.__segmented_nuclei.shape
        self.__arc_z_size, self.__arc_x_size, self.__arc_y_size = self.__arc_signal.shape
        print "Loaded images " + str(arcfile) + str(filename)

    def overlap(self):
        print "     Multiplying stacks."
        for i in range(0, self.__nuc_z_size):
            self.__overlap_stack[i] = ((self.__arc_stack[i, ...])*(self.__segmented_nuclei[i, ...]))
        print "     Overlap created"