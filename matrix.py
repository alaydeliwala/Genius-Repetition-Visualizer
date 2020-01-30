import requests
import time
from bs4 import BeautifulSoup
import numpy as lin_alg
import os
# Using regex to get client information
import re
import simple_chalk as chalk

BASE_URL = "http://api.genius.com"


def loadCredentials():
    """
        Loads the credentials from the credentials.txt file
        Credentials can be generated using the Genius API Management Site

        :return the users Genius client id, client secret and client access token
    """
    # Makes the contents of the file into a list
    credentials = [line.rstrip('\n') for line in open('credentials.txt')]

    # Loops through the file to look for the specified information
    for line in credentials:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]

        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]

        # This is the only one that matters untill OAuth2 can be implemented
        if "client_access_token" in line:
            client_access_token = re.findall(
                r'[\"\']([^\"\']*)[\"\']', line)[0]

    # Checks to see if credentials have been set
    if(not client_secret or not client_access_token or not client_access_token):
        error_message(
            "client_id, client_secret or client_access_token in credentials.txt is not set.")

    # Returns the credentials
    return client_id, client_secret, client_access_token


def error_message(message):
    """
        Prints error messages to the user
    """
    print(chalk.red("[Error]: ") + str(message))
    exit(1)


def searchSong(song_name, token):
    """
        Seraches for a song using the Genius API

        :param song_name - the name of the song to search
        :param token - the Genius authorization token
        :return the url for the song
    """

    edited_song_name = song_name.replace(" ", "%20")
    url = BASE_URL + '/search?q=' + edited_song_name
    response = requests.get(url, headers={"Authorization": 'Bearer ' + token})

    if(response.status_code != 200):
        error_message("Status Code: " +
                      str(response.status_code) + response.body)

    # Checks to make sure there are hits on the song name
    if len(response.json()['response']['hits']) != 0:
        # Gets the api_path of the song
        path = response.json()['response']['hits'][0]['result']['api_path']
        # Gets the name of the song
        name = response.json()['response']['hits'][0]['result']['full_title']
        return path, name
    else:
        error_message(
            "The song you searched for does not exist in the Spotify song catalog")


def getLyrics(path, token):
    """
        Gets the lyrics for the specified song

        :param path - the url path to the song in the Spotify Website
        :param token - the Spotify Authentication token
        :return the lyrics of the song
    """
    song_url = BASE_URL + path
    response = requests.get(
        song_url, headers={"Authorization": 'Bearer ' + token})
    lyrics_path = response.json()['response']['song']['path']
    # Going to the genius page to get the lyrics for the song
    page_url = "http://genius.com" + lyrics_path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")

    [h.extract for h in html('script')]

    lyrics = html.find("div", class_="lyrics").get_text()
    return lyrics


def main():
    print(">> welcome to this repetition analyzer")
    song_name = input(">> what song would you like to visualize?\n")
    print(">> loading required credentials")
    client_access_code, client_secure_code, client_auth_token = loadCredentials()
    print(">> searching through " + chalk.yellow("Genius"))
    path, name = searchSong(song_name, client_auth_token)
    print(">> match found -> \033[0;32m" + name + "\033[0m")
    print(">> scraping lyrics and removing common words")
    lyrics = getLyrics(path, client_auth_token)
    print(">> creating the self-similarity matrix")
    lyrics_list = re.split("\n| (|) | |, | ,", lyrics)
    temp_list = []
    for item in lyrics_list:
        if item != None and item != '':
            temp_list.append(item)
    lyrics_list = temp_list
    matrix = lin_alg.zeros((len(lyrics_list), len(lyrics_list)))

    ppmfile = open("repetition-matrix.ppm", 'w+')  # note the binary flag
    ppmfile.write("%s\n" % ('P3'))
    ppmfile.write("%d %d\n" % (len(lyrics_list), len(lyrics_list)))
    ppmfile.write("255\n")

    print(">> creating " + chalk.blue("repetition-matrix.ppm") + " file")
    out = 0
    ins = 0
    while out < len(lyrics_list):
        while ins < len(lyrics_list):
            if(lyrics_list[out] == lyrics_list[ins]):
                ppmfile.write("178 34 34 ")
                matrix[out, ins] = 1
                matrix[ins, out] = 1
            else:
                ppmfile.write("225 225 225 ")

            ins = ins+1
        ins = 0
        out = out+1
    ppmfile.seek(0, 2)
    size = ppmfile.tell()
    ppmfile.truncate(size - 1)
    ppmfile.seek(0, 2)
    ppmfile.write("\n")
    print(">> " + chalk.green("complete"))


if (__name__ == "__main__"):
    main()
