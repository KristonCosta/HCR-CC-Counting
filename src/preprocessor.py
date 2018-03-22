import numpy as np
import cv2
from skimage import filters
import skimage.io as io 

class Preprocessor:

    __image = None

    def __init__(self, filename):
        self.__image = io.imread(filename)

    def apply_adaptive_thresholding(self, image, apply_blur=True):
        z_size, _, _ = image.shape
        isolated_image = np.copy(image)
        for i in range(0,z_size):
            if apply_blur:
                isolated_image[i] = cv2.GaussianBlur(image[i],(3,3), 2)
            isolated_image[i] = cv2.adaptiveThreshold(isolated_image[i], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                cv2.THRESH_BINARY, 61, 0)
            image[i] = image[i] * isolated_image[i]
            image[i][image[i] > 0] = 1
        print "     Applied adaptive thresholding."
        return image

    
    def apply_erosion(self, image):
        z_size, _, _ = image.shape
        kernel = np.ones((2,2), np.uint8)
        for i in range(0,z_size):
            image[i] = cv2.morphologyEx(image[i], cv2.MORPH_OPEN, kernel)
        print "     Applied morphological opening."
        return image

    def apply_otsu_thresholding(self, image):
        image_filter = filters.threshold_otsu(image)
        isolated_image = image > image_filter
        image_mask = isolated_image.astype(int)
        print "     Applied Otsu thresholding."
        return image_mask

    def get_image(self):
        return self.__image

    def preprocess_basefile(self):
        print "\033[1m >>>>>>>>>> Preprocessing Base Image <<<<<<<<<< \033[0m"
        image = self.apply_adaptive_thresholding(self.__image)
        return image

    def preprocess_arcfile(self):
        print "\033[1m >>>>>>>>>> Preprocessing Arc Image <<<<<<<<<< \033[0m"
        image = self.apply_erosion(self.__image)
        image = self.apply_otsu_thresholding(image)
        return image 
