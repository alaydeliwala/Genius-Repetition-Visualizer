# Using regex to get client information
import re
from typing import NoReturn, Tuple, Dict, Any, List

import dotenv
import numpy as lin_alg
import requests
import simple_chalk as chalk
from bs4 import BeautifulSoup, PageElement
from numpy import ndarray

BASE_URL: str = "http://api.genius.com"

JsonData = Dict[str, Any]


def error_message(message: str) -> NoReturn:
    """Prints error messages to the user."""
    print(chalk.red("[Error]:"), message)
    exit(1)


def search_song(song_name: str, token: str) -> Tuple[str, str]:
    """
        Searches for a song using the Genius API

        :param song_name - the name of the song to search
        :param token - the Genius authorization token
        :return the url for the song
    """

    edited_song_name: str = song_name.replace(" ", "%20")
    url: str = f"{BASE_URL}/search?q={edited_song_name}"

    response: requests.Response = requests.get(
        url,
        headers={
            "Authorization": f'Bearer {token}'
        }
    )

    if not response.ok:
        error_message(
            f"Status Code: {response.status_code}, {response.body}"
        )

    # Checks to make sure there are hits on the song name
    if not len(response.json()['response']['hits']):
        error_message(
            "The song you searched for does not exist in "
            "the Spotify song catalog"
        )

    result: JsonData = response.json()['response']['hits'][0]['result']
    return result['api_path'], result['full_title']


def get_lyrics(path: str, token: str) -> str:
    """
        Gets the lyrics for the specified song

        :param path - the url path to the song in the Spotify Website
        :param token - the Spotify Authentication token
        :return the lyrics of the song
    """
    song_url: str = BASE_URL + path

    response: requests.Response = requests.get(
        song_url,
        headers={
            "Authorization": f'Bearer {token}'
        }
    )

    lyrics_path: str = response.json()['response']['song']['path']

    # Going to the genius page to get the lyrics for the song
    page: requests.Response = requests.get(f"http://genius.com{lyrics_path}")

    html: BeautifulSoup = BeautifulSoup(page.text, "html.parser")

    lyrics_div: PageElement = html.find("div", class_="lyrics")

    if lyrics_div is None:
        error_message("No Lyrics Found...")

    return lyrics_div.get_text()


def create_ppm_file(matrix, lyrics_list: List[str]) -> None:
    """Create a repetition matrix and save it to a ppm file."""
    print(">> creating", chalk.blue("repetition-matrix.ppm"), "file")

    with open("repetition-matrix.ppm", 'w+') as ppm_file:
        ppm_file.write(f"P3\n{len(lyrics_list)} {len(lyrics_list)}\n255\n")

        for out, lyric_out in enumerate(lyrics_list):
            for ins, lyric_ins in enumerate(lyrics_list):
                if lyric_out == lyric_ins:
                    ppm_file.write("178 34 34 ")

                    matrix[out, ins] = 1
                    matrix[ins, out] = 1

                else:
                    ppm_file.write("225 225 225 ")

        ppm_file.seek(0, 2)
        size = ppm_file.tell()
        ppm_file.truncate(size - 1)
        ppm_file.seek(0, 2)
        ppm_file.write("\n")


def main() -> None:
    print(">> welcome to this repetition analyzer")
    song_name: str = input(">> what song would you like to visualize?\n")
    print(">> loading required credentials")

    credentials = dotenv.dotenv_values('.env')

    if any(token is None for token in credentials.values()):
        error_message(
            "client_id, client_secret or client_access_token"
            " in credentials.txt is not set."
        )
        return

    print(">> searching through", chalk.yellow("Genius"))
    path, name = search_song(
        song_name,
        credentials["client_access_token"]
    )

    print(">> match found ->", chalk.green(name))
    print(">> scraping lyrics and removing common words")

    lyrics: str = get_lyrics(
        path,
        credentials["client_access_token"]
    )

    lyrics_list: List[str] = list(
        filter(bool, re.split("\n| (|) | |, | ,", lyrics))
    )

    print(">> creating the self-similarity matrix")

    # note the binary flag
    matrix: ndarray = lin_alg.zeros(
        (len(lyrics_list), len(lyrics_list))
    )

    create_ppm_file(matrix, lyrics_list)

    print(">>", chalk.green("complete"))


if __name__ == "__main__":
    main()
