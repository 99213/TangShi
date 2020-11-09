from django.http import JsonResponse
import re


def image_road(abs_road):
    road = re.findall(r"media/.+", abs_road)[0]
    return road


def file_type(file_name):
    fileType = file_name.replace(re.findall(r".*\.", file_name)[0], '.')[0]
    return fileType
