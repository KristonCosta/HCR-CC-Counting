import skimage.io as io
from scipy import ndimage
from skimage.morphology import closing
from skimage.morphology import opening
from skimage.filters import threshold_li, gaussian, threshold_mean, threshold_minimum, threshold_isodata

class Arcpreprocess:

    __x_size = -1
    __y_size = -1
    __z_size = -1

    __arc_stack = None

    def __init__(self, arcfile):
        self.__arc_stack = io.imread(arcfile)
        self.__z_size, self.__x_size, self.__y_size = self.__arc_stack.shape
        print "Loaded image " + str(arcfile)

    def apply_morphological_closing(self):
        print "     Starting morphological closing."
        for i in range(0, self.__z_size):
            self.__arc_stack[i] = closing(self.__arc_stack[i, ...])
        print "     Finished morphological closing"

    def apply_morphological_opening(self):
        print "     Starting morphological opening."
        for i in range(0, self.__z_size):
            self.__arc_stack[i] = opening(self.__arc_stack[i, ...])
        print "     Finished morphological opening"

    def apply_gaussian_filter(self):
        print "      Starting gaussian filter."
        for i in range(0, self.__z_size):
            self.__arc_stack[i] = gaussian(self.__arc_stack[i, ...])
        print "     Finished gaussian filter"

    def apply_mean_thresholding(self):
        image_filter = threshold_li(self.__arc_stack)
        isolated_image = self.__arc_stack < image_filter
        self.__arc_stack = isolated_image
        print "     Applied mean threshold filter."



    def run_arcpreprocess(self):
        print "\033[1m >>>>>>>>>> Running Preprocessor <<<<<<<<<< \033[0m"
        #self.apply_morphological_closing()
        #self.apply_morphological_opening()
        #self.apply_gaussian_filter()
        #self.apply_mean_thresholding()
        return self.__arc_stack

    def get_image_stack(self):
        return self.__arc_stack