# Using regex to get client information
import re

import dotenv
import numpy as lin_alg
import requests
import simple_chalk as chalk
from bs4 import BeautifulSoup

BASE_URL = "http://api.genius.com"


def error_message(message):
    """
        Prints error messages to the user
    """
    print(chalk.red("[Error]: ") + str(message))
    exit(1)


def search_song(song_name, token):
    """
        Seraches for a song using the Genius API

        :param song_name - the name of the song to search
        :param token - the Genius authorization token
        :return the url for the song
    """

    edited_song_name = song_name.replace(" ", "%20")
    url = BASE_URL + '/search?q=' + edited_song_name
    response = requests.get(url, headers={"Authorization": 'Bearer ' + token})

    if response.status_code != 200:
        error_message(
            "Status Code: " + str(response.status_code) + response.body
        )

    # Checks to make sure there are hits on the song name
    if len(response.json()['response']['hits']) == 0:
        error_message(
            "The song you searched for does not exist in "
            "the Spotify song catalog"
        )

    result = response.json()['response']['hits'][0]['result']
    print(result)
    return result['api_path'], result['full_title']


def get_lyrics(path, token):
    """
        Gets the lyrics for the specified song

        :param path - the url path to the song in the Spotify Website
        :param token - the Spotify Authentication token
        :return the lyrics of the song
    """
    print(path, token)

    song_url = BASE_URL + path

    response = requests.get(
        song_url, headers={"Authorization": 'Bearer ' + token}
    )

    lyrics_path = response.json()['response']['song']['path']

    # Going to the genius page to get the lyrics for the song
    page_url = "http://genius.com" + lyrics_path
    page = requests.get(page_url)

    html = BeautifulSoup(page.text, "html.parser")
    lyrics_div = html.find("div", class_="lyrics")

    if lyrics_div is None:
        error_message("No Lyrics Found...")

    return lyrics_div.get_text()


def main():
    print(">> welcome to this repetition analyzer")
    song_name = input(">> what song would you like to visualize?\n")
    print(">> loading required credentials")

    credentials = dotenv.dotenv_values('.env')

    if any(
            token is None for token in credentials.values()
    ):
        error_message(
            "client_id, client_secret or client_access_token"
            " in credentials.txt is not set."
        )
        return

    print(">> searching through " + chalk.yellow("Genius"))
    path, name = search_song(song_name, credentials["client_access_token"])
    print(">> match found -> \033[0;32m" + name + "\033[0m")
    print(">> scraping lyrics and removing common words")
    lyrics = get_lyrics(path, credentials["client_access_token"])
    print(">> creating the self-similarity matrix")
    lyrics_list = re.split("\n| (|) | |, | ,", lyrics)

    temp_list = [item for item in lyrics_list if item not in [None, '']]
    lyrics_list = temp_list
    matrix = lin_alg.zeros((len(lyrics_list), len(lyrics_list)))

    # note the binary flag
    ppmfile = open("repetition-matrix.ppm", 'w+')

    ppmfile.write("%s\n" % ('P3'))
    ppmfile.write("%d %d\n" % (len(lyrics_list), len(lyrics_list)))
    ppmfile.write("255\n")

    print(">> creating " + chalk.blue("repetition-matrix.ppm") + " file")

    for out in range(len(lyrics_list)):
        for ins in range(len(lyrics_list)):
            if lyrics_list[out] == lyrics_list[ins]:
                ppmfile.write("178 34 34 ")
                matrix[out, ins] = 1
                matrix[ins, out] = 1
            else:
                ppmfile.write("225 225 225 ")

    ppmfile.seek(0, 2)
    size = ppmfile.tell()
    ppmfile.truncate(size - 1)
    ppmfile.seek(0, 2)
    ppmfile.write("\n")

    print(">> " + chalk.green("complete"))


if __name__ == "__main__":
    main()
