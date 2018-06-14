# Genius-Repetition-Visualizer

## About
This repetition analyzer takes in a sing name and creates an image that represents the word repetition throught the song. The output is in a `picture.ppm` file
## Setup
### Auto Installation using pip!

1. Make sure you have installed virtualen, or if not then run `pip3 install virtualenv`
2. Create the python three virtual enviroment `virtualenv venv`
3. Start the enviroment `source venv/bin/activate`
4. Automatically install all relevant dependencies using the following command `pip install -r requirements.txt`
### Manul Installation
1. Make sure you have installed virtualen, or if not then run `pip3 install virtualenv`
2. Create the python three virtual enviroment `virtualenv venv`
 3. Start the enviroment `source myvenv/bin/activate`
 4. Install the pyton requests package `pip install requests`
5. Install numpy (linear algebra package) `pip install numpy`
6. Install bs4 (Beautiful Soup 4) `pip install bs4`
*Make sure all downloaded items are for Python 3.x*
## Usage
In the root folder of the program run this command to start the virtual enviorment
```shell
$ source venv/bin/activate
```
After the virtual enviorment has strted run this command to start the program
```shell
$ python matrix.py
```
*Try not to make a spelling mistake when typing the song name*

## Shoutouts

 - Shoutout to @genius for being the world's greatest public knowledge project since Wikipedia and making all their information avalible to us through their amazing public API :notes: :books: 
 - Shoutout to [SongSim](https://colinmorris.github.io/SongSim/#/) for the original analysis idea :heart_eyes:
 - Shoutout to [requests](https://github.com/requests/requests-oauthlib) for a great HTTP and OAuth2 tool for humans ✨🍰✨
