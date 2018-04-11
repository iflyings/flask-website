# -*- coding: UTF-8 -*-
import os
import re

FOLDER_HEAD = "./app/static/resource/"
URL_HEAD = "/static/resource/"

class Repository:

    def __init__(self, app=None):
        if hasattr(app, 'repository'):
            self.__cartoonInfo = app.repository['cartoonInfo']
            self.__imageInfo = app.repository['imageInfo']

    def init_app(self, app):
        if app and not hasattr(app, 'repository'):
            cartoon_info = self.__create_cartoon_info()
            _, image_info = self.__create_image_info(1, "#", FOLDER_HEAD + "image/", URL_HEAD + "image/")
            app.repository = {
                'cartoonInfo': cartoon_info,
                'imageInfo': image_info
            }
            self.__cartoonInfo = app.repository['cartoonInfo']
            self.__imageInfo = app.repository['imageInfo']
    """
    漫画
    """
    @staticmethod
    def __create_cartoon_list(folder_path, url_path):
        file_list = sorted(filter(
            lambda f: os.path.isfile(folder_path + f) and re.search("(.jpg|.png)$", f, re.I),
                                   os.listdir(folder_path)))
        if file_list:
            return list(map(lambda file: url_path + file, file_list))

    @staticmethod
    def __create_cartoon_info():
        cartoon_info = []
        folder_list = sorted(filter(lambda f: os.path.isdir(FOLDER_HEAD + "cartoon/" + f),
                                    os.listdir(FOLDER_HEAD + "cartoon/")))
        for index, folder in enumerate(folder_list):
            map_info = dict()
            map_info["id"] = index + 1
            map_info["text"] = folder.split(" ")[0]
            map_info["list"] = Repository.__create_cartoon_list(
                                    FOLDER_HEAD + "cartoon/" + folder + "/",
                                    URL_HEAD + "cartoon/" + folder + "/")
            if map_info["list"]:
                cartoon_info.append(map_info)
        return cartoon_info

    def get_cartoon_name(self, page_id):
        for cartoon in self.__cartoonInfo:
            if page_id == cartoon["id"]:
                return cartoon["text"]

    def get_cartoon_info(self):
        cartoon_info = []
        for info in self.__cartoonInfo:
            cartoon_info.append({
                "id": info["id"],
                "text": info["text"]
            })
        return cartoon_info

    def get_cartoon_count(self, page_id):
        for cartoon in self.__cartoonInfo:
            if page_id == cartoon["id"]:
                return len(cartoon["list"])
        return 0

    def get_cartoon_list(self, page_id, index, length):
        for cartoon in self.__cartoonInfo:
            if page_id == cartoon["id"]:
                if index + length >= len(cartoon["list"]):
                    length = len(cartoon["list"]) - index
                if length > 0:
                    return cartoon["list"][index:index+length]
    """
    图片
    """
    @staticmethod
    def __create_image_list(folder_path, url_path):
        image_list = sorted(filter(lambda file: os.path.isfile(folder_path + file),
                                   os.listdir(folder_path)))
        if image_list:
            image_list = filter(lambda file: re.search("(.jpg|.png)$", file, re.I), image_list)
            image_list = list(map(lambda file: url_path + file, image_list))
            if 0 < len(image_list):
                return image_list
        return []

    @staticmethod
    def __create_image_info(index, parent_info, folder_path, url_path):
        image_info = []
        folder_list = sorted(filter(lambda f: os.path.isdir(folder_path + f),
                                    os.listdir(folder_path)))
        if folder_list:
            for folder in folder_list:
                map_info = dict()
                map_info["id"] = str(index)
                map_info["parent"] = parent_info
                map_info["text"] = folder
                map_info["list"] = Repository.__create_image_list(folder_path + folder + "/", url_path + folder + "/")
                image_info.append(map_info)
                index = index + 1
                index, list = Repository.__create_image_info(index, map_info["id"],
                                                             folder_path + folder + "/",
                                                             url_path + folder + "/")
                if list is not None:
                    image_info = image_info + list
            return index, image_info
        return index, None

    def get_image_name(self, page_id):
        for cartoon in self.__imageInfo:
            if page_id == cartoon["id"]:
                return cartoon["text"]

    def get_image_info(self):
        image_info = []
        for info in self.__imageInfo:
            image_info.append({
                "id": info["id"],
                "parent": info["parent"],
                "text": info["text"]
            })
        return image_info

    def get_image_list(self, page_id):
        for image in self.__imageInfo:
            if page_id == image["id"]:
                return image["list"]
        return []
