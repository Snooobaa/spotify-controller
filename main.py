import tkinter as tk
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load .env file to environment
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

# Global variables for GIF animation
playing = False
current_frame = 0
frames = []

# Tkinter setup
def play_music():
    global playing
    sp.start_playback()
    playing = True
    animate_gif()  # Start GIF animation when music is playing

def pause_music():
    global playing
    sp.pause_playback()
    playing = False  # Stop playing music and GIF animation

def load_gif():
    global frames
    try:
        # Load all frames of the GIF
        frames = [tk.PhotoImage(file='dance.gif', format=f'gif -index {i}') for i in range(27)] 
        if frames:
            print("GIF loaded successfully!")
        else:
            print("GIF loading failed: No frames found")
    except Exception as e:
        print(f"Error loading GIF: {e}")

def animate_gif():
    global current_frame
    if playing and frames:  # Ensure that the GIF frames are loaded and music is playing
        current_frame = (current_frame + 1) % len(frames)
        gif_label.config(image=frames[current_frame])
        root.after(100, animate_gif)  # Loop GIF frames with a 100ms delay

def update_current_song():
    try:
        current_playback = sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track = current_playback['item']
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            current_song_label.config(text=f"Now playing: {song_name} by {artist_name}")
        else:
            current_song_label.config(text="No song is currently playing")
    except Exception as e:
        current_song_label.config(text="Error fetching song data")
        print(f"Error in update_current_song: {e}")
    root.after(1000, update_current_song)

# Function to initialize playing state based on Spotify playback
def initialize_playing_state():
    global playing
    try:
        current_playback = sp.current_playback()
        if current_playback and current_playback['is_playing']:
            playing = True  # Music is already playing
            gif_label.config(image=frames[0])  # Display the first frame of the GIF immediately
            animate_gif()  # Start GIF animation if music is playing
        else:
            playing = False  # Music is not playing
        print(f"Initial playback state: {'Playing' if playing else 'Paused'}")
    except Exception as e:
        print(f"Error initializing playback state: {e}")
        playing = False  # Default to paused if there's an error

# Main window setup
root = tk.Tk()
root.title("Spotify Controller")

# Play button
play_button = tk.Button(root, text="Play", command=play_music)
play_button.pack(pady=10)

# Pause button
pause_button = tk.Button(root, text="Pause", command=pause_music)
pause_button.pack(pady=10)

# Gif label
gif_label = tk.Label(root)
gif_label.pack(pady=10)

# Load the GIF when the app starts
load_gif()

# Current song label
current_song_label = tk.Label(root, text="No song is currently playing")
current_song_label.pack(pady=10)

# Initialize playing state based on Spotify playback
initialize_playing_state()

# Start updating the current song
update_current_song()

# Run the Tkinter event loop
root.mainloop()
