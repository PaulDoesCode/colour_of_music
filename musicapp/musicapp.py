# Colour of Music (musicapp.py)
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
import vlc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from musicdata import musicData
from lightdata import lightData

# set Spotify dev credentials to to allow API access
os.environ["SPOTIPY_CLIENT_ID"] = "8d71cede506c4af3bcad36f6730a3155"
os.environ["SPOTIPY_CLIENT_SECRET"] = "6e1ae6771a314a44bc391520f04c1891"

# musicApp class
class musicApp():

    # constructor for musicApp object
    def __init__(self, window):

        # instantiate spotify variable to enable API access using client credentials
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

        # instantiate bridge variable to create lightData object 
        self.bridge = lightData()

        # instantiate search result variables
        self.result1 = None
        self.result2 = None
        self.result3 = None

        # display and positioning for the album/single/EP image used
        self.img = Label(window, image = "")
        self.img.place(x = 250, y = 130, anchor = "center")

        # display and positioning for the track and mapping details
        self.trackInfo = Label(window, text = "")
        self.trackInfo.place(x = 120, y = 260)

        # display and positioning for the text entry field
        self.txtFld = Entry(window, text ="", bd = 5)
        self.txtFld.place(x = 120, y = 290)

        # display and positioning for the search button
        self.btn = Button(window, text="Search", command=self.searchForMusic)
        self.btn.place(x = 120, y = 330)

        # display and positioning for first search result
        self.searchResult1 = Button(window, text="Search Result 1", command=lambda:self.analyseTrack(self.result1))
        self.searchResult1.place(x = 120, y = 370)

        # display and positioning for second search result
        self.searchResult2 = Button(window, text="Search Result 2", command=lambda:self.analyseTrack(self.result2))
        self.searchResult2.place(x = 120, y = 400)

        # display and positioning for third search result
        self.searchResult3 = Button(window, text ="Search Result 3", command=lambda:self.analyseTrack(self.result3))
        self.searchResult3.place(x = 120, y = 430)

        # create button to exit application and close window
        self.quitButton = Button(window, text="Quit App", command=self.endProgram)
        self.quitButton.place(x = 120, y = 470)

    # function to search for song
    # gets information from text entry field
    # user search will produce 3 search results and each one can be selected
    def searchForMusic(self):
        
        # trackObj is an array of tracks gathered from the user search query
        trackObj = self.spotify.search(self.txtFld.get(), type="track")

        # first search result
        # result1 = retrieves track information
        # searchResult1 = retrieves artist and song name from track information, later displayed on-screen
        # same applies for search results 2 and 3
        self.result1 = musicData(trackObj["tracks"]["items"][0])
        self.searchResult1["text"] = self.result1.artistName + "-" + self.result1.trackName

        # second search result
        self.result2 = musicData(trackObj["tracks"]["items"][1])
        self.searchResult2["text"] = self.result2.artistName + "-" + self.result2.trackName

        # third search result
        self.result3 = musicData(trackObj["tracks"]["items"][2])
        self.searchResult3["text"] = self.result3.artistName + "-" + self.result3.trackName

    # function to analyse track information and produce a result
    def analyseTrack(self, selectedResult):

        # retrieve track cover details (i.e. album/single/EP cover image)
        # urllib is used to open the url from Spotify and read in the image
        rawImage = urllib.request.urlopen(selectedResult.trackImageUrl).read()
        imageFullName = ImageTk.PhotoImage(Image.open(io.BytesIO(rawImage)).resize((250, 250), Image.ANTIALIAS))
        self.img.config(image = imageFullName)
        self.img.photo_ref = imageFullName

        # retrieve track uri, assign to variable
        # print track uri for testing purposes
        trackUri = selectedResult.trackUri

        # retrieve track name, assign to variable
        selectedTrackName = selectedResult.trackName

        # retrieve artist genre
        genre = self.spotify.artist(selectedResult.artistUrl)

        # retrieve energy and valence for the selected track
        features = self.spotify.audio_features([trackUri]) 
        energy = features[0]["energy"]
        valence = features[0]["valence"]

        # play 30 second track preview
        player = vlc.MediaPlayer(selectedResult.trackPreviewUrl)
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
        # Philips uses colour wheel to determine coordinates with a hue scale of 0-65535 (seen in lightData class)
        # use percentages to determine colour (hue) choice and attached emotion
        if valence < 0.5 and energy > 0.5:
            colour = "Red"
            emotion = "Angry"
            self.bridge.setAngryTrackColour()
        if valence > 0.5 and energy > 0.5:
            colour = "Green"
            emotion = "Happy"
            self.bridge.setHappyTrackColour()
        if valence > 0.5 and energy < 0.5:
            colour = "Blue"
            emotion = "Calm"
            self.bridge.setCalmTrackColour()
        if valence < 0.5 and energy < 0.5:
            colour = "Purple"
            emotion = "Sad"
            self.bridge.setSadTrackColour()
        
        # print artist genres
        # print energy and valence values in console
        # print chosen colour in console
        print("artist genre: ", genre["genres"])
        print("valence - " + str(valence))
        print("energy - " + str(energy))
        print("light - " + colour)   

        # used to print track and mapping details on-screen
        self.trackInfo.config(text = selectedTrackName + " - " + colour + " (" + emotion + ")")

    # function to end program
    # window.destroy() exits application and closes window
    # turn light off when finished
    def endProgram(self):
        window.destroy()
        self.bridge.turnLightOff()

# extra GUI code
# make new window using tkinter
window = Tk()

# GUI title
window.title('Colour of Music')

label = Label(window, text="")
label.place(x=80, y=10)

# GUI size dimensions
window.geometry("500x700")

# create application object
musicApp = musicApp(window)

# execute window functionality when application is run
# i.e. create application window
window.mainloop()