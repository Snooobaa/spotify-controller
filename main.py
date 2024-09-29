import tkinter as tk
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

#load .env file to environment
load_dotenv()

# Spotify setup
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

scope = "user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# Tkinter setup
def play_music():
    sp.start_playback()

def pause_music():
    sp.pause_playback()

# Main window
root = tk.Tk()
root.title("Spotify Controller")

# Play button
play_button = tk.Button(root, text="Play", command=play_music)
play_button.pack(pady=10)

# Pause button
pause_button = tk.Button(root, text="Pause", command=pause_music)
pause_button.pack(pady=10)

root.mainloop()
