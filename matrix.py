import requests
import time
from bs4 import BeautifulSoup
import numpy as lin_alg
import os

# Using regex to get client information
import re

BASE_URL = "http://api.genius.com"

DISPLAY_WIDTH = 32 * 1 #32 pixels x 1 displays
DISPLAY_HEIGHT = 16

# Loads the credentials from the credentials.ini file
# Credentials can be goten from the Genius API Management Site
def loadCredentials():
    # Makes the contents of the file into a list
    credentials = [line.rstrip('\n') for line in open ('credentials.ini')]
    # Loops through the file to look for the specified information
    for line in credentials:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        # This is the only one that matters untill OAuth2 can be implemented
        if "client_access_token" in line:
            client_access_token = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
    # Returns the credentials
    return client_id, client_secret, client_access_token

# Search for the song
# Returns the path too the song
def searchSong(song_name, token):
    edited_song_name = song_name.replace(" ", "%20");
    url = BASE_URL + '/search?q='+ edited_song_name
    response = requests.get(url, headers={"Authorization": 'Bearer ' + token})

    # Makes sure that the request is going through
    # print(response.status_code)

    # Checks to make sure there are hits on the song name
    if len(response.json()['response']['hits']) != 0:
        # Gets the api_path of the song
        # Need to check if result is matched
        path = response.json()['response']['hits'][0]['result']['api_path']
        return path

# Gets the lyrics for the specified song
def getLyrics(path, token):
    song_url = BASE_URL + path
    response = requests.get(song_url, headers={"Authorization": 'Bearer ' + token})
    lyrics_path = response.json()['response']['song']['path']
    #Going to the genius page to get the lyrics for the song
    page_url = "http://genius.com" + lyrics_path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")

    [h.extract for h in html('script')]

    lyrics = html.find("div", class_= "lyrics").get_text()
    return lyrics

def main():
    print (">> welcome to this repetition analyzer")
    print (">> loading required credentials")
    client_access_code, client_secure_code, client_auth_token = loadCredentials()

    song_name = input(">> what song would you like to visualize?\n")
    lyrics = ''
    print(">> searching for " + song_name)
    path = searchSong(song_name, client_auth_token)
    if path:
        print(">> scraping lyrics for " + song_name)
        lyrics = getLyrics(path,client_auth_token)
        print(lyrics)
    else:
        print(">> no songs matched")
    lyrics_list = re.split("\n| (|) | |, | ,", lyrics)
    temp_list = []
    for item in lyrics_list:
        if item != None and item != '':
            temp_list.append(item)
    lyrics_list = temp_list
    matrix = lin_alg.zeros((len(lyrics_list), len(lyrics_list)))

    screen = [[0,0,0] for x in range(DISPLAY_WIDTH*DISPLAY_HEIGHT)]
    ppmfile=open("picture.ppm",'w+') # note the binary flag
    ppmfile.write("%s\n" % ('P3'))
    ppmfile.write("%d %d\n" % (len(lyrics_list), len(lyrics_list)))
    ppmfile.write("255\n")

    # out = 0;
    # ins = 0;
    # while out < len(lyrics_list):
    #     while ins < len(lyrics_list):
    #         if(lyrics_list[out] == lyrics_list[ins]):
    #             matrix[out,ins] = 1
    #             matrix[ins,out] = 1
    #         ins=ins+1
    #     ins = 0
    #     out=out+1

    out = 0;
    ins = 0;
    while out < len(lyrics_list):
        while ins < len(lyrics_list):
            if(lyrics_list[out] == lyrics_list[ins]):
                ppmfile.write("178 34 34 " )
                matrix[out,ins] = 1
                matrix[ins,out] = 1
            else:
                ppmfile.write("225 225 225 ")

            ins=ins+1
        ins = 0
        out=out+1
    ppmfile.seek(0,2)
    size = ppmfile.tell()
    ppmfile.truncate(size - 1)
    ppmfile.seek(0,2)
    ppmfile.write("\n")

if (__name__ == "__main__") : main()