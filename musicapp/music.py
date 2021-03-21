# Colour of Music (music.py)
# GCU Honours Project
# by Paul Harbison-Smith (S1712745)

# import external libraries
import os
from tkinter import *
from phue import Bridge
import math
import requests
import vlc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

os.environ["SPOTIPY_CLIENT_ID"] = "8d71cede506c4af3bcad36f6730a3155"
os.environ["SPOTIPY_CLIENT_SECRET"] = "6e1ae6771a314a44bc391520f04c1891"

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

window = Tk()
# add widgets here

# GUI title
window.title('Colour of Music')

window.geometry("300x200+10+20")

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
    label.config(text=txtfld.get())
    print(spotify.search(txtfld.get(), type="track"))
    trackObj=spotify.search(txtfld.get(), type="track")
    print(trackObj)
    print(trackObj["tracks"]["items"][0]["uri"])
    trackUri=trackObj["tracks"]["items"][0]["uri"]
    print(spotify.audio_features([trackUri]))
    features=spotify.audio_features([trackUri]) 
    energy=features[0]["energy"]
    valence=features[0]["valence"]
    print("valence - " + str(valence))
    print("energy - " + str(energy))
    preview_url=trackObj["tracks"]["items"][0]["preview_url"]
    print(preview_url)
    preview=requests.get(preview_url)
    print(preview)
    player=vlc.MediaPlayer(preview_url)
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

artistName=Label(window, text="")
label.place(x=120, y=20)

topSong=Label(window, text="")
label.place(x=80, y=30)

btn = Button(window, text="Search", command=txtfldGet)
btn.place(x=120, y=100)
txtfld = Entry(window, text="", bd=5)
txtfld.place(x=80, y=150)

window.mainloop()