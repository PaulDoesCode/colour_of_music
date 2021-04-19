# Colour of Music (musicdata.py)
# GCU Honours Project
# by Paul Harbison-Smith (S1712745)

# musicData class
class musicData:

    # constructor for musicData object
    def __init__(self, result):
        self.artistName = result["artists"][0]["name"]
        self.trackName = result["name"]
        self.trackUri = result["uri"]
        self.trackImageUrl = result["album"]["images"][0]["url"]
        self.artistUrl = result["artists"][0]["external_urls"]["spotify"]
        self.trackPreviewUrl = result["preview_url"]
