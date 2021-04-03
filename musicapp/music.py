# Colour of Music (music.py)
# GCU Honours Project
# by Paul Harbison-Smith (S1712745)

# import external libraries
import os
from tkinter import *
from phue import Bridge
import math
from PIL import Image, ImageFilter, ImageTk
import urllib
import io
import requests
import vlc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

os.environ["SPOTIPY_CLIENT_ID"] = "8d71cede506c4af3bcad36f6730a3155"
os.environ["SPOTIPY_CLIENT_SECRET"] = "6e1ae6771a314a44bc391520f04c1891"

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

window = Tk()

# GUI title
window.title('Colour of Music')

window.geometry("600x400+10+20")

result1 = None
result2 = None
result3 = None

label = Label(window, text="")
label.place(x=80, y=10)

# create Bridge variable for Hue Bridge
b = Bridge("192.168.0.73")

# connect to Bridge
b.connect()

# get API info from Bridge
b.get_api()
print(b.get_api())

b.get_light(1, 'on')

b.get_light(1, 'name')
print(b.get_light(1, 'name'))

# 65535 limit for hue
b.set_light(1, 'bri', 150)
b.set_light(1, 'hue', math.floor(3300))
    
# search for song
# get information from text entry field
# use information to retrieve song data
def txtfldGet():
    label.config(text = txtfld.get())
    print(spotify.search(txtfld.get(), type="track"))
    trackObj = spotify.search(txtfld.get(), type="track")

    global result1 
    result1 = trackObj["tracks"]["items"][0]
    global searchResult1
    searchResult1["text"] = result1["artists"][0]["name"] + "-" + result1["name"]

    global result2 
    result2 = trackObj["tracks"]["items"][1]
    global searchResult2
    searchResult2["text"] = result2["artists"][0]["name"] + "-" + result2["name"]

    global result3 
    result3 = trackObj["tracks"]["items"][2]
    global searchResult3
    searchResult3["text"] = result3["artists"][0]["name"] + "-" + result3["name"]

def analyseTrack(selectedResult):
    print(selectedResult)

    global img
    print(img) 
    rawImage = urllib.request.urlopen(selectedResult["album"]["images"][0]["url"]).read()
    imageFullName = ImageTk.PhotoImage(Image.open(io.BytesIO(rawImage)))
    img.config(image = imageFullName)
    img.photo_ref = imageFullName

    trackUri = selectedResult["uri"]
    print(spotify.audio_features([trackUri]))

    features = spotify.audio_features([trackUri]) 
    energy = features[0]["energy"]
    valence = features[0]["valence"]

    print("valence - " + str(valence))
    print("energy - " + str(energy))

    preview_url=selectedResult["preview_url"]
    print(preview_url)

    preview = requests.get(preview_url)
    print(preview)

    player = vlc.MediaPlayer(preview_url)
    player.play()

    # initialise variable "colour"
    colour=None 

    # Valence = X-axis
    # Energy = Y-axis
    # red = high energy, negative sound (low valence, high energy)
    # green = high energy, positive sound (high valence, high energy)
    # blue = low energy, positive sound (high valence, low energy)
    # purple = low energy, negative sound (low valence, low energy)
    # Philips uses colour wheel to determine coordinates, use radians to determine colour choice
    if valence < 0.5 and energy > 0.5:
        colour = "red"
        b.set_light(1, 'hue', math.floor(0))
    if valence > 0.5 and energy > 0.5:
        colour = "green"
        b.set_light(1, 'hue', math.floor(65535/3))
    if valence > 0.5 and energy < 0.5:
        colour = "blue"
        b.set_light(1, 'hue', math.floor(65535/1.67))
    if valence < 0.5 and energy < 0.5:
        colour = "purple"
        b.set_light(1, 'hue', math.floor(65535/1.33))
    print(colour)   

artistName = Label(window, text="")
label.place(x = 120, y = 20)

topSong = Label(window, text = "")
label.place(x = 80, y = 30)

img = Label(window, image = "")
img.place(x = 0, y = 0)

btn = Button(window, text="Search", command=txtfldGet)
btn.place(x = 120, y = 100)

searchResult1 = Button(window, text="1", command=lambda:analyseTrack(result1))
searchResult1.place(x = 120, y = 140)

searchResult2 = Button(window, text="2", command=lambda:analyseTrack(result2))
searchResult2.place(x = 120, y = 180)

searchResult3 = Button(window, text ="3", command=lambda:analyseTrack(result3))
searchResult3.place(x = 120, y = 220)

txtfld = Entry(window, text ="", bd = 5)
txtfld.place(x = 80, y = 50)

window.mainloop()