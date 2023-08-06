import requests
import os
from sys import argv
from tv_models import TVShow
from tv_cache import cache

CACHE_TIMEOUT = 60 * 5
URL = "https://api.tvmaze.com/search/shows?q="

if __name__ == "__main__" or __name__ == "tv_program":

    def search_show(show_name):
        response = requests.get(URL, f"q={show_name}")

        if not response.json():
            raise ValueError

        results = response.json()

        for result in results:
            if result["show"]["name"] == show_name:
                return result["show"]
        raise ValueError

    @cache(ttl=CACHE_TIMEOUT)
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

    def main():
        show_name = read_show_name()
        show_info = get_show_info(show_name)
        print(*show_info, sep="\n")

