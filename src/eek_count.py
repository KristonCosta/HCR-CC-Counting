from colour_generator import ColourGenerator
from preprocessor import Preprocessor
from segmenter import Segmenter
from analysis import Analysis
import numpy as np
import scipy.misc
import time
import os
import sys

class EekCounter:
    
    arcfile = "resources/633smallbetter.tif"
    basefile = "resources/568smallbetter.tif"

    cell_aggragation_shape = (2,7,7)
    enable_debugging = True

    def __init__(self, user_basefile=None):
        if user_basefile:
            self.name = user_basefile
        self.colour_generator = ColourGenerator()

    def run(self):
        base_preprocessor = Preprocessor(self.basefile)
        base_preprocessed_image_stack = base_preprocessor.preprocess_basefile()
        arc_preprocessor = Preprocessor(self.arcfile)
        arc_preprocessed_image_stack = arc_preprocessor.preprocess_arcfile()

        x, y, z = self.cell_aggragation_shape
        segmenter = Segmenter(base_preprocessed_image_stack, self.create_np_ellipsoid(x, y, z), 
                "WS", generate_debugging=self.enable_debugging)
        segmented_image_stack = segmenter.run_segmentation()

        analysis = Analysis(segmented_image_stack, arc_preprocessed_image_stack)
        analysis.generate_report()
        colorized_image_stack = analysis.colorize_overlapping_cells()
        self.save_image_stack(colorized_image_stack)


    def save_image_stack(self, image_stack):
        print "\033[1m >>>>>>>>>> Saving Stack <<<<<<<<<< \033[0m"
        z_size, _, _, _, = image_stack.shape
        base_name = "resources"
        folder_name = "%s/stack" % base_name
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        for i in range(0, z_size):
            name = "%s/stack%s.tif" % (folder_name, i)
            slice_of_stack = image_stack[i, ...]
            scipy.misc.toimage(slice_of_stack).save(name)
        self.__saved_folder_name = "%s_%d" % (self.basefile.split(".")[0], int(time.time()))
        os.rename(folder_name, self.__saved_folder_name)

    def create_np_ellipsoid(selfs, width, length, height):
        np_elipse = np.zeros((height*2+1, length*2+1, width*2+1))
        a_2 = float(length * length)
        b_2 = float(width * width)
        c_2 = float(height * height)
        for x in range(-length, length+1):
            for y in range(-width,width+1):
                for z in range(-height, height+1):
                    np_elipse[z + height][x + length][y + width] = ((x*x)/a_2 + (y*y/b_2) + (z*z/c_2) <= 1)
        return np_elipse

if __name__ == "__main__":
    eek_counter = EekCounter()
    eek_counter.run()

