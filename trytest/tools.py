from django.http import JsonResponse
import re


def image_road(abs_road):
    road = re.findall(r"media/.+", abs_road)[0]
    return road


def file_type(file_name):
    fileType = re.match(r".*(\..*)", file_name).groups()[0]
    return fileType
