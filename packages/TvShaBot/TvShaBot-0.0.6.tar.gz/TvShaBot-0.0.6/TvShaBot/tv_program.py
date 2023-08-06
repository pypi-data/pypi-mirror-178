import requests
import os
from sys import argv
from TvShaBot.tv_models import TVShow

URL = "https://api.tvmaze.com/search/shows?q="

def search_show(show_name):
        response = requests.get(URL, f"q={show_name}")

        if not response.json():
            raise ValueError

        results = response.json()

        for result in results:
            if result["show"]["name"] == show_name:
                return result["show"]
        raise ValueError

def get_show_info(show_name):
    show_uv = search_show(show_name)
    show = TVShow(**show_uv)
    return show.info()

def read_show_name():
    is_read = False
    result = ""
    file = os.path.basename(__file__)

    for param in argv:
        if is_read:
            result += " " * bool(result) + param
        else:
            if (
                len(param) < len(file) or param[-len(file):] != file
            ) and param != "-m":
                continue
            else:
                is_read = True

    if result:
        return result
    else:
        raise ValueError
