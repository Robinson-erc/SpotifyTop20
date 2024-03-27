import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Spotify API credentials
client_id = "e9fb00b2739c4107843e3cd0fb2e4cef"
client_secret = "47be381b7b7740d699d088fc36ddcf26"
spotipy_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=spotipy_credentials)

# Function to get the top 20 tracks for the selected genre
def get_top_20_tracks(genre):
    results = sp.search(q=f'genre:"{genre}"', type='track', limit=20)
    tracks = results['tracks']['items']
    return tracks

# Function to plot tracks
def plot_tracks(genre, tracks):
    # Extract track names and popularity scores
    track_names = [track['name'] for track in tracks]
    popularity_scores = [track['popularity'] for track in tracks]

    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.bar(track_names, popularity_scores, color='skyblue')
    plt.xlabel('Track')
    plt.ylabel('Popularity Score')
    plt.title(f'Top 20 Tracks in {genre.capitalize()} Genre')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Function to handle the submit button click event
def submit_genre():
    genre = genre_entry.get().strip()
    if genre:
        # If the genre is provided, proceed with the action (e.g., plot)
        top_20_tracks = get_top_20_tracks(genre)
        if not top_20_tracks:
            messagebox.showinfo("No Tracks Found", f"No tracks found for the specified genre '{genre}'. Please try again.")
        else:
            # Proceed with plotting or any other action
            plot_tracks(genre, top_20_tracks)
    else:
        messagebox.showwarning("Missing Genre", "Please enter a genre.")

# Create the main Tkinter window
root = tk.Tk()
root.title("Top Tracks by Genre")

# Create a label asking the user to enter a genre
genre_label = tk.Label(root, text="Enter a genre such as 'pop', 'hip-hop', 'rock', etc.:")
genre_label.pack(pady=10)

# Create an entry widget for the user to input the genre
genre_entry = tk.Entry(root, width=30)
genre_entry.pack(pady=5)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit_genre)
submit_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
