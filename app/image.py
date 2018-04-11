# -*- coding: UTF-8 -*-

import os

def get_image_info(page_index):
    if type(page_index) == str:
        page_index = int(page_index)
    page_index = page_index - 1
    image_info_list = sorted(filter(lambda f: os.path.isdir("./app/static/resource/" + f),
                                  os.listdir("./app/static/resource/")))
    if page_index <= len(image_info_list):
        image_list = os.listdir("./app/static/resource/" + image_info_list[page_index])
        image_info = {
            'total': len(image_info_list),
            'index': page_index + 1,
            'title': image_info_list[page_index],
            'list': sorted(map(lambda file: "/static/resource/" + image_info_list[page_index] + "/" + file,
                             image_list))
        }
        return image_info
