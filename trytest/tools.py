from django.http import JsonResponse
import re


def image_road(abs_road):
    road = re.findall(r"media/.+", abs_road)[0]
    return road


def file_type(file_name):
    a = re.findall(r"\..*\.", file_name)

    fileType = re.findall(r"\..*", file_name)[0]
    if len(a) > 0:
        fileType = fileType.replace(a[0], '.')
    return fileType
