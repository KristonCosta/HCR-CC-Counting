import skimage.io as io
import numpy as np
from scipy import ndimage
from skimage import filters
from skimage import exposure
import sys
import time

class Preprocessor:

    __x_size = -1
    __y_size = -1
    __z_size = -1

    __image_stack = None
    __window_size = 0

    def __init__(self, filename, user_window_size=8):
        self.__image_stack = io.imread(filename)
        self.__z_size, self.__x_size, self.__y_size = self.__image_stack.shape
        self.__window_size = user_window_size
        print "Loaded image " + str(filename)

    def apply_median_filter(self):
        print "     Median filtering %d slices." % self.__z_size
        for i in range(0, self.__z_size):
            self.__image_stack[i] = ndimage.median_filter(self.__image_stack[i, ...], self.__window_size)
        print "     Finished median filtering %s slices." % self.__z_size

    def apply_otsu_filter(self):
        image_filter = filters.threshold_otsu(self.__image_stack)
        isolated_image = self.__image_stack < image_filter
        self.__image_stack = isolated_image
        print "     Applied Otsu filter."

    def apply_intensity_normalization(self):
        for j in range(0, self.__z_size):
            self.__image_stack[j] = exposure.equalize_adapthist(self.__image_stack[j, ...], clip_limit=2)
        print "     Finished intensity normalization"

    def run_preprocessor(self):
        print "\033[1m >>>>>>>>>> Running Preprocessor <<<<<<<<<< \033[0m"
        self.apply_median_filter()
        self.apply_otsu_filter()
        self.apply_intensity_normalization()
        return self.__image_stack

    def get_image_stack(self):
        return self.__image_stack
