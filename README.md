# Genius-Repetition-Visualizer

## About
This repetition analyzer can search for any song through the genius API and then creates an image from the songs self-similarity matrix

<p align = "center"><a href="url"><img src="https://github.com/alaydeliwala/Genius-Repetition-Visualizer/blob/master/img/barbie.png?raw=true" height="250" width="250"></a></p>

Given a text of length n tokens, it constructs an n x n matrix, where (i, j) is filled in if the ith and jth words are the same (after some normalization).

The output available in a `repetition-matrix.ppm` file

<p align="center">
    <img src="https://github.com/alaydeliwala/Genius-Repetition-Visualizer/blob/master/img/Holy%20Grail%20by%20JAY-Z%20(Ft.%20Justin%20Timberlake).png" width="275" />
</p>

<p align="center">
    <strong>Holy Grail</strong> (Ft. Justin Timberlake) by Jay-Z
</p>

## Setup
### Getting Access to the Genius API
To use this program you must create a `.env` to contain your Genius API credentials.
Copy the `.env.example` file and fill your Api Credentials in.

[Click here to create Genius Api Credentials](https://genius.com/api-clients)
### Auto Installation using pip!

1. Make sure you have installed virtualen, or if not then run `pip3 install virtualenv`
2. Create the python three virtual environment `virtualenv venv`
3. Start the environment `source venv/bin/activate`
4. Automatically install all relevant dependencies using the following command `pip install -r requirements.txt`
### Manul Installation
1. Make sure you have installed virtualen, or if not then run `pip3 install virtualenv`
2. Create the python three virtual environment `virtualenv venv`
 3. Start the environment `source venv/bin/activate`
 4. Install the python requests package `pip install requests`
5. Install numpy (linear algebra package) `pip install numpy`
6. Install bs4 (Beautiful Soup 4) `pip install bs4`
*Make sure all downloaded items are for Python 3.x*
## Usage
<p align = "center"><a href="url"><img src="https://github.com/alaydeliwala/Genius-Repetition-Visualizer/blob/master/img/working.gif" width="700"></a></p>

In the root folder of the program run this command to start the virtual environment
```shell
$ source venv/bin/activate
```
After the virtual environment has started run this command to start the program
```shell
$ python matrix.py
```
*Try not to make a spelling mistake when typing the song name*

## Shoutouts

 - Shoutout to @genius for being the world's greatest public knowledge project since Wikipedia and making all their information avalible to us through their amazing public API :notes::books:
 - Shoutout to [SongSim](https://colinmorris.github.io/SongSim/#/) for the original analysis idea :heart_eyes:
 - Shoutout to [requests](https://github.com/requests/requests-oauthlib) for a great HTTP and OAuth2 tool for humans ✨🍰✨
