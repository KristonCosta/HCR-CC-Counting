from colour_generator import ColourGenerator
from preprocessor import Preprocessor
from segmenter import Segmenter
import numpy as np
import scipy.misc
import time
import os
import sys

class EekCounter:

    __saved_folder_name = None

    median_window_size = 8
    segmenter_type = "WS"
    aggregate_cube_size = np.ones((20, 20, 20))
    filename = "resources/sytox_seg_test_stack_zoom_new.tif"

    def __init__(self, user_filename=None):
        if user_filename:
            self.filename = user_filename
        self.colour_generator = ColourGenerator()

    def run(self):

        preprocessor = Preprocessor(self.filename, self.median_window_size)
        preprocessed_image_stack = preprocessor.run_preprocessor()

        segmenter = Segmenter(preprocessed_image_stack, self.aggregate_cube_size, self.segmenter_type)
        segmented_image_stack = segmenter.run_segmentation()

        colorized_image_stack = self.colorize_image_stack(segmented_image_stack)
        self.save_image_stack(colorized_image_stack)

        self.generate_report(segmented_image_stack)


    def generate_report(self, segmented_image_stack):
        print "\033[1m >>>>>>>>>> Final Report <<<<<<<<<< \033[0m"
        cell_count = self.count_cells(segmented_image_stack)
        print ">>> Folder name: " + self.__saved_folder_name
        print ">>> Total number of unique cells found: " + str(cell_count)

    def colorize_image_stack(self, segmented_image_stack):
        print "\033[1m >>>>>>>>>> Colourizing Stack <<<<<<<<<< \033[0m"
        color_generator = ColourGenerator()
        z_size, x_size, y_size = segmented_image_stack.shape
        colorized = np.ndarray(shape=(z_size, x_size, y_size, 4), dtype=int)
        for x in range(0, x_size):
            for y in range(0, y_size):
                for z in range(0, z_size):
                    colorized[z][x][y] = color_generator.get_colour_for_segment(segmented_image_stack[z][x][y])
        return colorized

    def save_image_stack(self, image_stack):
        print "\033[1m >>>>>>>>>> Saving Stack <<<<<<<<<< \033[0m"
        z_size, _, _, _ = image_stack.shape
        base_name = "resources"
        folder_name = "%s/stack" % base_name
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        for i in range(0, z_size):
            name = "%s/stack%s.tif" % (folder_name, i)
            slice_of_stack = image_stack[i, ...]
            scipy.misc.toimage(slice_of_stack).save(name)
        self.__saved_folder_name = "%s_%d" % (self.filename.split(".")[0], int(time.time()))
        os.rename(folder_name, self.__saved_folder_name)

    def count_cells(self, segmented_image_stack):
        return len(np.unique(segmented_image_stack))-1

if __name__ == "__main__":
    eek_counter = EekCounter()
    eek_counter.run()

