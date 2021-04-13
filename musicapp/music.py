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

# set Spotify dev credentials to to allow API access
os.environ["SPOTIPY_CLIENT_ID"] = "8d71cede506c4af3bcad36f6730a3155"
os.environ["SPOTIPY_CLIENT_SECRET"] = "6e1ae6771a314a44bc391520f04c1891"
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# create Bridge variable for Philips Hue Bridge
# connect to Bridge using IP address
b = Bridge("192.168.0.73")

# connect to Bridge
b.connect()

# get API info from Bridge
b.get_api()

# turn light on
b.set_light(1, 'on', True)

# check if light is on or off
b.get_light(1, 'on')

# get light name
b.get_light(1, 'name')

# 0-65535 hue scale for hue lightbulb
# 0-254 brightness scale for hue lightbulb
# set initial light brightness and hue
b.set_light(1, 'bri', 254)
b.set_light(1, 'hue', math.floor(50))

# initialise search result variables for music search
result1 = None
result2 = None
result3 = None

# function to search for song
# gets information from text entry field
# user search will produce 3 search results and each one can be selected
def txtfldGet():
    trackObj = spotify.search(txtfld.get(), type="track")

    # first search result
    global result1 
    result1 = trackObj["tracks"]["items"][0]
    global searchResult1
    searchResult1["text"] = result1["artists"][0]["name"] + "-" + result1["name"]

    # second search result
    global result2 
    result2 = trackObj["tracks"]["items"][1]
    global searchResult2
    searchResult2["text"] = result2["artists"][0]["name"] + "-" + result2["name"]

    # third search result
    global result3 
    result3 = trackObj["tracks"]["items"][2]
    global searchResult3
    searchResult3["text"] = result3["artists"][0]["name"] + "-" + result3["name"]

# function to analyse track information and produce a result
def analyseTrack(selectedResult):

    # retrieve track cover details (i.e. album/single/EP cover image)
    # urllib is used to open the url from Spotify and read in the image
    global img
    rawImage = urllib.request.urlopen(selectedResult["album"]["images"][0]["url"]).read()
    imageFullName = ImageTk.PhotoImage(Image.open(io.BytesIO(rawImage)).resize((250, 250), Image.ANTIALIAS))
    img.config(image = imageFullName)
    img.photo_ref = imageFullName

    # retrieve track uri, assign to variable
    # print track uri for testing purposes
    trackUri = selectedResult["uri"]
    print(spotify.audio_features([trackUri]))

    # retrieve track name, assign to variable
    selectedTrackName = selectedResult["name"]

    # retrieve artist genre
    genre = spotify.artist(selectedResult["artists"][0]["external_urls"]["spotify"])

    # retrieve energy and valence for the selected track
    features = spotify.audio_features([trackUri]) 
    energy = features[0]["energy"]
    valence = features[0]["valence"]

    # retrieve track preview URL (30 second track preview)
    preview_url=selectedResult["preview_url"]
    preview = requests.get(preview_url)

    # play 30 second track preview
    player = vlc.MediaPlayer(preview_url)
    player.play()

    # instantiate colour variable
    colour = None 

    # instantiate emotion variable
    emotion = None

    # Valence = X-axis
    # Energy = Y-axis
    # red = high energy, negative sound (low valence, high energy)
    # green = high energy, positive sound (high valence, high energy)
    # blue = low energy, positive sound (high valence, low energy)
    # purple = low energy, negative sound (low valence, low energy)
    # Philips uses colour wheel to determine coordinates with a hue scale of 0-65535
    # use radians to determine colour (hue) choice and attached emotion
    if valence < 0.5 and energy > 0.5:
        colour = "Red"
        emotion = "Angry"
        b.set_light(1, 'hue', math.floor(0))
    if valence > 0.5 and energy > 0.5:
        colour = "Green"
        emotion = "Happy"
        b.set_light(1, 'hue', math.floor(65535/3))
    if valence > 0.5 and energy < 0.5:
        colour = "Blue"
        emotion = "Calm"
        b.set_light(1, 'hue', math.floor(65535/1.67))
    if valence < 0.5 and energy < 0.5:
        colour = "Purple"
        emotion = "Sad"
        b.set_light(1, 'hue', math.floor(65535/1.33))
    
    # print artist genres
    # print energy and valence values in console
    # print chosen colour in console
    print("artist genre: ", genre["genres"])
    print("valence - " + str(valence))
    print("energy - " + str(energy))
    print("light - " + colour)   

    # used to print track and mapping details on-screen
    trackInfoLabel.config(text = selectedTrackName + " - " + colour + " (" + emotion + ")")

# GUI code
# make new window using tkinter
window = Tk()

# GUI title
window.title('Colour of Music')

label = Label(window, text="")
label.place(x=80, y=10)

# GUI size dimensions
window.geometry("500x700+10+20")

# display and positioning for the album/single/EP image used
img = Label(window, image = "")
img.place(x = 250, y = 130, anchor = "center")

# display and positioning for the track and mapping details
trackInfoLabel = Label(window, text = "")
trackInfoLabel.place(x = 120, y = 260)

# display and positioning for the text entry field
txtfld = Entry(window, text ="", bd = 5)
txtfld.place(x = 120, y = 290)

# display and positioning for the search button
btn = Button(window, text="Search", command=txtfldGet)
btn.place(x = 120, y = 330)

# display and positioning for first search result
searchResult1 = Button(window, text="Search Result 1", command=lambda:analyseTrack(result1))
searchResult1.place(x = 120, y = 370)

# display and positioning for second search result
searchResult2 = Button(window, text="Search Result 2", command=lambda:analyseTrack(result2))
searchResult2.place(x = 120, y = 400)

# display and positioning for third search result
searchResult3 = Button(window, text ="Search Result 3", command=lambda:analyseTrack(result3))
searchResult3.place(x = 120, y = 430)

# function to end program
# window.destroy() exits application and closes window
# turn light off when finished
def endProgram():
    window.destroy()
    b.set_light(1, 'on', False)

# create button to exit application and close window
quitButton = Button(window, text="Quit App", command=endProgram)
quitButton.place(x = 120, y = 470)

# execute window functionality when application is run
# i.e. create application window
window.mainloop()