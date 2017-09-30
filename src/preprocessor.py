import skimage.io as io
import numpy as np
from scipy import ndimage
from skimage import filters
from skimage.morphology import closing, erosion, dilation

from skimage.segmentation import random_walker
from skimage import exposure
import sys
import time

class Preprocessor:

    __x_size = -1
    __y_size = -1
    __z_size = -1

    __image_stack = None
    __window_size = 0
    __filter_type = "M"

    def __init__(self, filename, user_window_size=8, filter_type="M"):
        self.__filter_type = filter_type
        self.__image_stack = io.imread(filename)
        self.__z_size, self.__x_size, self.__y_size = self.__image_stack.shape
        self.__window_size = user_window_size
        print "Loaded image " + str(filename)

    def apply_gaussian_filter(self):
        print "      Gaussian filtering %d slices." % self.__z_size
        for i in range(0, self.__z_size):
            self.__image_stack[i] = filters.gaussian(-self.__image_stack[i, ...], sigma=0.1)
        print "     Finished gaussian filtering %s slices." % self.__z_size

    def apply_median_filter(self, user_window_size = None):
        if not user_window_size:
            user_window_size = self.__window_size
        print "     Median filtering %d slices." % self.__z_size
        for i in range(0, self.__z_size):
            self.__image_stack[i] = ndimage.median_filter(self.__image_stack[i, ...], user_window_size)
        print "     Finished median filtering %s slices." % self.__z_size

    def apply_morphological_closing(self):
        print "     Doing morphological closing."
        for i in range(0, self.__z_size):
            self.__image_stack[i] = closing(self.__image_stack[i,...])
        print "     Finished morphological closing"

    def apply_otsu_filter(self):
        image_filter = filters.threshold_otsu(self.__image_stack)
        isolated_image = self.__image_stack < image_filter
        self.__image_stack = isolated_image
        print "     Applied Otsu filter."

    def apply_silly_filter(self):
        print "     Applying silly filter~~~."
        markers = np.zeros(self.__image_stack.shape, dtype=np.uint)
        for i in range(0, self.__z_size):
            self.__image_stack[i] = closing(self.__image_stack[i], np.ones((3, 3)))
           # self.__image_stack[i] = dilation(self.__image_stack[i], np.ones((2, 2)))
            markers[i][self.__image_stack[i] < 50] = 1
            markers[i][self.__image_stack[i] > 210] = 2

        self.__image_stack = random_walker(self.__image_stack, markers, beta=5, mode='bf')

    def run_preprocessor(self):
        print "\033[1m >>>>>>>>>> Running Preprocessor <<<<<<<<<< \033[0m"
        if self.__filter_type == "G":
            self.apply_gaussian_filter()
        elif self.__filter_type == "M":
            self.apply_median_filter()
        else:
            raise Exception("Supported filters are G (Gaussian) and M (Median).")
      #  self.apply_morphological_closing()
        self.apply_otsu_filter()
        return self.__image_stack

    def get_image_stack(self):
        return self.__image_stack
