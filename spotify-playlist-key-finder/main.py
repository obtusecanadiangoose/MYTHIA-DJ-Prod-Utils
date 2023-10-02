import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

def get_spotify_playlist_tracks(playlist_url):
    # Set up Spotify API credentials
    with open(".spotify_creds.json", "r") as file:
        creds = json.load(file)
    client_id = creds["client_id"]
    client_secret = creds["client_secret"]
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Extract playlist ID from the URL
    playlist_id = playlist_url.split('/')[-1]
    #playlist_id = '0S0cuX8pnvmF7gA47Eu63M'
    
    # Retrieve playlist tracks
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    
    # Continue pagination if necessary
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    playlist_songs = []
    for i in range(len(tracks)):
        if i != 0:
            track_name = tracks[i]['track']['name']
            track_artists = ""
            for artist in (tracks[i]['track']['album']['artists']):
                track_artists += artist['name']+" "
                break #freemp3 works better with only one artist name
            full = track_artists+track_name

            duration_ms=tracks[i]['track']['duration_ms']
            track_min = str(int(duration_ms)/60000)
            track_sec = str(float(track_min[1:])*60)
            if track_sec[1] == ".":
                track_sec = "0"+track_sec[0]
            trackadd = (full, "0"+track_min[0]+":"+track_sec[:2])
            playlist_songs.append(trackadd)    
    
    return playlist_songs

# Example usage
#playlist_url = 'http://open.spotify.com/playlist/0S0cuX8pnvmF7gA47Eu63M' #reddit.com/r/edm weekly playlist
#playlist_url = 'http://open.spotify.com/playlist/0xyqpMVkAmo6HNOpbZGMm2'
#playlist_url = 'https://open.spotify.com/playlist/7HubxREQJciZEOYY8CBi5D' #My Secret Sky Playlist
playlist_url = 'https://open.spotify.com/playlist/3imvWy8mfgTiLfikvOav1x'

songs = get_spotify_playlist_tracks(playlist_url)

print(songs)
    

