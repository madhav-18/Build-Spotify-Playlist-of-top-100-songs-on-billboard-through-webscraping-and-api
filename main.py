import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID_SPOTIFY = "Your Spotify Client ID"
CLIENT_SECRET_SPOTIFY = "Your Spotify Client Secret Key"
URL_REDIRECT = "http://example.com"
URL = "https://www.billboard.com/charts/hot-100"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"{URL}/{date}")
soup = BeautifulSoup(response.text, "html.parser")

all_songs = soup.select("li ul li h3")
song_name = [song.getText().strip() for song in all_songs]
# print(song_name)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=URL_REDIRECT,
        client_id=CLIENT_ID_SPOTIFY,
        client_secret=CLIENT_SECRET_SPOTIFY,
        show_dialog=True,
        cache_path="token.txt",
        username="NAME OF YOUR PROFILE",
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

song_uris = []
year = date.split("-")[0]
for song in song_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)