"""
Base module for the Animechan API. The documentation is available at
https://animechan.vercel.app/guide
"""
import typing
import requests

from anime_api import exceptions
from anime_api.apis.animechan.objects import Quote


class AnimechanAPI:
    """
    Docs: https://animechan.vercel.app/guide
    """

    endpoint = "https://animechan.vercel.app/api"

    def __init__(self, endpoint: typing.Optional[str] = None):
        self.endpoint = endpoint or self.endpoint

    def get_random_quote(self) -> Quote:
        """
        Get a random quote from the API.
        """
        response = requests.get(f"{self.endpoint}/random")

        AnimechanAPI.__check_response_code(response.status_code)

        return Quote(**response.json())

    def get_many_random_quotes(self) -> typing.List[Quote]:
        """
        Get 10 random quotes from the API.
        """
        response = requests.get(f"{self.endpoint}/quotes")

        AnimechanAPI.__check_response_code(response.status_code)

        return [Quote(**quote) for quote in response.json()]

    def search_by_anime_title(self, anime_title: str, page: int = 1) -> Quote:
        """
        Return a list of quotes from the given anime.
        """
        response = requests.get(
            f"{self.endpoint}/quotes/anime", params={"title": anime_title, "page": page}
        )

        AnimechanAPI.__check_response_code(response.status_code)

        return [Quote(**quote) for quote in response.json()]

    def search_by_character_name(self, character_name: str, page: int = 1) -> Quote:
        """
        Return a list of quotes from the given character.
        """
        response = requests.get(
            f"{self.endpoint}/quotes/character",
            params={"name": character_name, "page": page},
        )

        AnimechanAPI.__check_response_code(response.status_code)

        return [Quote(**quote) for quote in response.json()]

    def get_animes(self, page: int = 1) -> typing.List[str]:
        """
        Return a list of animes.
        """
        response = requests.get(
            f"{self.endpoint}/available/anime", params={"page": page}
        )

        AnimechanAPI.__check_response_code(response.status_code)

        return response.json()

    @staticmethod
    def __check_response_code(status_code: int, msg: str = ""):
        if status_code == 404:
            raise exceptions.NotFound(status_code, msg=msg)
        elif status_code != 200:
            raise exceptions.ServerError(status_code=status_code, msg=msg)
