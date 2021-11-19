import json
import time
from secrets import *
import lyricsgenius
from lyricsgenius import Genius
import spotipy
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=scid, client_secret=scsecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
token = util.prompt_for_user_token(susername, scope, scid, scsecret, sredirectURI)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print(f"Could not find token for {susername}.")

def currentTrackInfo():
    currentTrack = sp.current_user_playing_track()
    
    artist = currentTrack['item']['artists'][0]['name']
    song = currentTrack['item']['name']
    uri = currentTrack['item']['uri']

    return artist, song, uri

def getCurrentTrackLyrics(currentArtist, currentSong, currentURI):
    uri = None
    while True:
        currentArtist, currentSong, currentURI = currentTrackInfo()
        if uri != currentURI:
            print("--------------------------------")
            uri = currentURI
            genius = Genius(gtoken)
            song = genius.search_song(currentSong, currentArtist)
            
            if song != None:
                print(song.lyrics.replace("EmbedShare URLCopyEmbedCopy", ""))
                
                saveLyrics = input("Would you like to save these lyrics? Type 'Y' or 'y' to save: ")
                
                if saveLyrics == "Y" or saveLyrics == "y":
                    with open(f"{currentArtist} - {currentSong}.txt", "w") as f:
                        f.write(song.lyrics.replace("EmbedShare URLCopyEmbedCopy", ""))
                    print("--------------------------------")
                    print(f"Lyrics written into {currentArtist} - {currentSong}.txt!")
                    continue
                else:
                    print("--------------------------------")
                    print("Lyrics not saved.")
                    continue
            else:
                print("Lyrics not found.")
                
def run():
    print("--------------------------------")
    print("*** BE SURE TO EITHER BE PLAYING MUSIC FROM AN ALBUM, PLAYLIST, OR QUEUE. ***")
    print("This program is sensitive to small intervals of time between songs, so \nmake sure you are able to minimize that period of time as much as possible.")
    print("Otherwise, you risk crashing the program.")
    time.sleep(8)
    currentArtist, currentSong, currentURI = currentTrackInfo()
    getCurrentTrackLyrics(currentArtist, currentSong, currentURI)

run()