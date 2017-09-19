from scipy import ndimage
from skimage.feature import peak_local_max
from skimage import morphology
from skimage.morphology import watershed
import numpy as np

class Segmenter:

    __image_stack = None
    __processed_stack = None
    __distance_stack = None

    __aggregate_cube_size = (0, 0, 0)

    __debugging_dictionary = {}
    __debugging_list = []
    __generate_debugging = False

    __segmenter_type = ""

    def __init__(self, user_image_stack, user_aggregate_cube_size=np.ones((20, 20, 20)),
                 user_segmenter_type="WS", distance_inverse=True, generate_debugging=False):
        self.__image_stack = user_image_stack
        if distance_inverse:
            self.__image_stack = -self.__image_stack
        self.__processed_stack = self.__image_stack
        self.__aggregate_cube_size = user_aggregate_cube_size
        self.__generate_debugging = generate_debugging
        self.__segmenter_type = user_segmenter_type

    def __add_to_debug(self, step_name, stack):
        if self.__generate_debugging:
            self.__debugging_list.append(step_name)
            self.__debugging_dictionary[step_name] = stack

    def run_segmentation(self):
        print "\033[1m >>>>>>>>>> Running Segmenter <<<<<<<<<< \033[0m"
        self.calculate_distance()
        self.generate_maxi()
        self.generate_markers()
        if self.__segmenter_type == "WS":
            self.generate_watershed()
        elif self.__segmenter_type == "RW":
            self.generate_random_walk()
        else :
            raise Exception("Supported segmenters are WS (watershed) and RW (random-walk).")
        return self.__processed_stack

    def calculate_distance(self):
        self.__distance_stack = ndimage.distance_transform_edt(self.__image_stack)
        self.__add_to_debug("distance", self.__distance_stack)
        print "     Generated distance transform."

    def generate_maxi(self):
        self.__processed_stack = peak_local_max(self.__distance_stack, indices=False,
                                                footprint=self.__aggregate_cube_size, exclude_border=False,
                                                labels=self.__image_stack)
        self.__add_to_debug("maxi", self.__processed_stack)
        print "     Generated local maxi."

    def generate_markers(self):
        self.__processed_stack = morphology.label(self.__processed_stack)
        self.__add_to_debug("markers", self.__processed_stack)
        print "     Generated markers."

    def generate_watershed(self):
        self.__processed_stack = watershed(-self.__distance_stack, self.__processed_stack, mask=self.__image_stack)
        self.__add_to_debug("watershed", self.__processed_stack)
        print "     Generated watershed segmentation."

    def generate_random_walk(self):
        # TODO: Put the random walk stuff here, take out exception when done
        raise Exception("You didn't implement random walk!")
        self.__add_to_debug("random_walk", self.__processed_stack)
        print "     Generated random walk segmentation."

    def get_debug_list(self):
        return self.__debugging_list

    def get_debug_stack(self, step_name):
        return self.__debugging_dictionary[step_name]
