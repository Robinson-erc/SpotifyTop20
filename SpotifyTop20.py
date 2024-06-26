import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import webbrowser

# Spotify API credentials
client_id = "e9fb00b2739c4107843e3cd0fb2e4cef"
client_secret = "47be381b7b7740d699d088fc36ddcf26"
spotipy_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=spotipy_credentials)

# Global variables to store track data
genre = ""
top_20_tracks = []
track_dropdown = None  # Global variable for track dropdown menu

# Function to get the top 20 tracks for the selected genre
def get_top_20_tracks(genre):
    results = sp.search(q=f'genre:"{genre}"', type='track', limit=20)
    tracks = results['tracks']['items']
    return tracks

# Function to handle the submit button click event
def submit_genre():
    global genre, top_20_tracks
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

# Function to plot tracks and create dropdown menu
def plot_tracks(genre, tracks):
    global track_dropdown  # Declare as global to modify it within the function
    # Extract track names and popularity scores
    track_names = [track['name'] for track in tracks]
    popularity_scores = [track['popularity'] for track in tracks]
    global track_urls
    track_urls = [track['external_urls']['spotify'] for track in tracks]

    # Plotting the graph
    plt.figure(figsize=(10, 6))
    bars = plt.bar(track_names, popularity_scores, color='#1DB954')  # Use Spotify green color
    plt.xlabel('Track')
    plt.ylabel('Popularity Score')
    plt.title(f'Top 20 Tracks in {genre.capitalize()} Genre')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()  # Automatically adjusts subplot parameters to give specified padding

    # Function to handle click event on bar
    def on_bar_click(event):
        if event.inaxes == plt.gca():
            for i, bar in enumerate(bars):
                if bar.contains(event)[0]:
                    url = track_urls[i]
                    webbrowser.open(url)

    # Connect the click event to the plot
    plt.gcf().canvas.mpl_connect('button_press_event', on_bar_click)

    # Add label to inform users that bars are clickable
    plt.text(0.5, 1.088, "Click on a bar to open the corresponding song on Spotify", ha='center', transform=plt.gca().transAxes, fontsize=10)

    # Create dropdown menu
    menu_frame = tk.Frame(root, bg='#191414')
    menu_frame.pack(pady=10)
    selected_track = tk.StringVar()
    selected_track.set("Select a track")
    track_dropdown = ttk.Combobox(menu_frame, textvariable=selected_track, values=track_names)
    track_dropdown.pack(padx=10, pady=5)
    open_track_button = tk.Button(menu_frame, text="Open Selected Track", command=open_selected_track, bg="#1db954", fg="white", font=("Arial", 12), relief=tk.FLAT)
    open_track_button.pack(pady=5)

    plt.show()

# Function to open selected track on Spotify
def open_selected_track():
    global track_dropdown  # Declare as global to access it
    selected_track_index = track_dropdown.current()
    if selected_track_index != -1:
        url = track_urls[selected_track_index]
        webbrowser.open(url)
    else:
        messagebox.showwarning("No Track Selected", "Please select a track from the dropdown menu.")

# Create the main Tkinter window
root = tk.Tk()
root.title("Top Tracks by Genre")

# Set the background color to Spotify's black color
root.configure(bg='#191414')

# Create a label asking the user to enter a genre
genre_label = tk.Label(root, text="Enter a genre such as 'pop', 'hip-hop', 'rock', etc.:", fg='#1DB954', bg='#191414', font=("Arial", 12, "bold"))
genre_label.pack(pady=10)

# Create an entry widget for the user to input the genre
genre_entry = tk.Entry(root, width=30)
genre_entry.pack(pady=5)

# Create a submit button with Spotify green color
submit_button = tk.Button(root, text="Submit", command=submit_genre, bg="#1db954", fg="white", font=("Arial", 12), relief=tk.FLAT)
submit_button.pack(pady=5)

# Load the Spotify logo image and resize it
spotify_logo_path = "spotify_logo.png"
spotify_logo_image = Image.open(spotify_logo_path)
spotify_logo_image = spotify_logo_image.resize((200, 200))  # Resize to desired dimensions
spotify_logo_photo = ImageTk.PhotoImage(spotify_logo_image)

# Create a label to display the resized Spotify logo with black background
spotify_logo_label = tk.Label(root, image=spotify_logo_photo, bg='#191414')
spotify_logo_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
