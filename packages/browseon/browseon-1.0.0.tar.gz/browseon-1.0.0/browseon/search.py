import os.path
import webbrowser
from srutil import util
from typing import Literal

from . import util as bu


class Browse:

    @staticmethod
    def open(url: str):
        """
        open url in default browser.

        :param url: url to open
        """
        url = Browse.__validate_url(url)
        webbrowser.open(url)

    @staticmethod
    def search(query: str,
               engine: Literal[
                   "google", "duckduckgo", "yahoo", "bing", "yandex", "qwant", "wikipedia", "youtube"] = "google"):
        """
        search for query in default browser.

        :param query: query to search
        :param engine: search engine
        """
        _url = Browse.__get_as_url(bu.encoded_query(query), engine)
        Browse.open(url=_url)

    @staticmethod
    def __get_as_url(query, web_engine) -> str:
        url = util.stringbuilder(bu.get_baseurl_for(web_engine), query, separator="+")
        return url

    @staticmethod
    def __validate_url(url) -> str:
        if not os.path.exists(url):
            if not url.startswith("http"):
                url = "https://" + url
            bu.is_valid_url(url)
        return url
