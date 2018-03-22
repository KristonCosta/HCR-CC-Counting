class ColourGenerator:

    # Usage:
    # c = ColourGenerator()
    # result = c.get_colour_for_segment(10)
    #
    # OR
    #
    # c = ColourGenerator([1,2,3,4], [1,2,3,5], [1,2,3,4]]) <--- Supply your own colour list
    # result = c.get_colour_for_segment(10)

    # __ means private! So they shouldn't show up during code completion and
    # you can't access them by going c.__colour_index
    __colour_index = 0
    __colour_list = [[255, 0, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255],
                   [255, 255, 0, 255], [255, 0, 255, 255], [0, 255, 255, 255],
                   [192, 192, 192, 255], [128, 0, 0, 255], [128, 128, 0, 255],
                   [0, 128, 0, 255], [128, 0, 128, 255], [0, 128, 128, 255],
                   [0, 0, 128, 255], [128, 128, 128, 255], [255, 69, 0, 255],
                   [0, 100, 0, 255], [102, 205, 170, 255], [176, 224, 230, 255],
                   [123, 104, 238, 255], [218, 112, 214, 255], [255, 182, 193, 255]]
    # Dictionary lookup for segment colors, start with black for 0 (background)
    __colour_map = {0: [0, 0, 0, 255], -1: [200, 200, 200, 255]}

    def __init__(self, user_colour_list=None):
        if user_colour_list:
            self.__colour_list = user_colour_list

    def get_colour_for_segment(self, segment_number):
        if segment_number not in self.__colour_map:
            if self.__colour_index >= len(self.__colour_list):
                self.__colour_index = 0
            self.__colour_map[segment_number] = self.__colour_list[self.__colour_index]
            self.__colour_index += 1
        return self.__colour_map[segment_number]

    def map_id_to_color(self, id_list):
        for i in id_list:
            self.get_colour_for_segment(i)
        return self.__colour_map