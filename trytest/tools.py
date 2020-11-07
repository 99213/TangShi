from django.http import JsonResponse
import re


def image_road(abs_road):
    road = re.findall(r"media/.+", abs_road)[0]
    return road
