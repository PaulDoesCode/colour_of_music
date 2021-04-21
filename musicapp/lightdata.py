# Colour of Music (lightdata.py)
# GCU Honours Project
# by Paul Harbison-Smith (S1712745)

# import external libraries
import math
from phue import Bridge

# lightData class
class lightData:
    
    # constructor for lightData object
    # connect to bridge, turn on light and set default light values
    def __init__(self):
        self.bridge = Bridge("192.168.0.73")
        self.bridge.connect()
        self.turnLightOn()
        self.setDefaultHue()

    # function to turn light on upon application startup
    def turnLightOn(self):
        self.bridge.set_light(1, 'on', True)

    # function to set default hue upon application startup
    def setDefaultHue(self):
        self.bridge.set_light(1, 'hue', 0)
        self.bridge.set_light(1, 'sat', 30)
        self.bridge.set_light(1, 'bri', 255)

    # Valence = X-axis
    # Energy = Y-axis
    # red = high energy, negative sound (low valence, high energy)
    # green = high energy, positive sound (high valence, high energy)
    # blue = low energy, positive sound (high valence, low energy)
    # purple = low energy, negative sound (low valence, low energy)
    # Philips uses colour wheel to determine coordinates with a hue scale of 0-65535
    # use percentages to determine colour (hue) choice and attached emotion

    # function to set light to red when track is deemed to be "angry"
    def setAngryTrackColour(self):
        self.bridge.set_light(1, 'hue', 0)
        self.bridge.set_light(1, 'sat', 255)

    # function to set light to green when track is deemed to be "happy"
    def setHappyTrackColour(self):
        self.bridge.set_light(1, 'hue', math.floor(65535*0.33))
        self.bridge.set_light(1, 'sat', 255)

    # function to set light to blue when track is deemed to be "calm"
    def setCalmTrackColour(self):
        self.bridge.set_light(1, 'hue', math.floor(65535*0.65))
        self.bridge.set_light(1, 'sat', 255)

    # function to set light to purple when track is deemed to be "sad"
    def setSadTrackColour(self):
        self.bridge.set_light(1, 'hue', math.floor(65535*0.75))
        self.bridge.set_light(1, 'sat', 255)

    # function to turn light off when user quits the application
    def turnLightOff(self):
        self.bridge.set_light(1, 'on', False)