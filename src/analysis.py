import numpy as np
from colour_generator import ColourGenerator
from collections import defaultdict

class Analysis:

	__base_image = None
	__arc_image = None
	__overlap_set = False
	__overlap_image = None

	def __init__(self, base, arc):
		self.__base_image = base
		self.__arc_image = arc 

	def find_overlap(self):
		print "     Finding cell and arc overlap."
		if not self.__overlap_set:
			self.__overlap_set = True
			self.__overlap_image = np.multiply(self.__base_image, self.__arc_image)
		return self.__overlap_image

	def colorize_overlapping_cells(self):
		print "\033[1m >>>>>>>>>> Colourizing Stack <<<<<<<<<< \033[0m"
		colour_generator = ColourGenerator()
		overlap = self.find_overlap()
		base_ids = np.unique(self.__base_image)

		color_ids = np.unique(overlap)
		num_color_ids = len(color_ids)
		print "     Generating color map."
		colour_map = colour_generator.map_id_to_color(color_ids)
		key_to_key = {}
		color_list = []
		index = 0
		for key in base_ids:
			if key == -1:
				continue
			if key in color_ids:
				color_list.append(colour_map[key])
				key_to_key[key] = index
				index += 1
			else:
				key_to_key[key] = num_color_ids
		color_list.append(colour_map[-1])
		key_to_key[-1] = num_color_ids
		print "     Applying color map."
		setting_color = np.vectorize(key_to_key.get)(self.__base_image)
		colorized = np.take(np.asarray(color_list), setting_color, axis = 0)
		return colorized

	def generate_report(self):
		print "\033[1m >>>>>>>>>> Final Report <<<<<<<<<< \033[0m"
		overlap_image = self.find_overlap()
		base_cell_count = self.count_cells(self.__base_image)
		overlap_cell_count = self.count_cells(overlap_image)
		print ">>> Total number of unique cells found: " + str(base_cell_count)
		print ">>> Total number of unique cells found: " + str(overlap_cell_count)

	def count_cells(self, image_stack):
		return len(np.unique(image_stack))-1
