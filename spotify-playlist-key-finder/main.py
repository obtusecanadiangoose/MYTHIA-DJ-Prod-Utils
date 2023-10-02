import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep

# Define the scope and load credentials from the JSON file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('.gspread_creds.json', scope)

# Authenticate with Google Sheets API
gc = gspread.authorize(credentials)

spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1U0gjNtjH9OibocBIuWEDiCHNVld1ILif9bGNC-MQjUA")


with open(".spotify_creds.json", "r") as file:
    creds = json.load(file)
client_id = creds["client_id"]
client_secret = creds["client_secret"]
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


key_mapping = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B'
}

camelot_mapping = {
    'CMaj':"8B",
    'C#Maj':"3B", #-5
    'DMaj':"10B", #+7
    'D#Maj':"5B",
    'EMaj':"12B",
    'FMaj':"7B",
    'F#Maj':"2B",
    'GMaj':"9B",
    'G#Maj':"4B",
    'AMaj':"11B",
    'A#Maj':"6B",
    'BMaj':"1B",
    'CMin':"5A",
    'C#Min':"12A",
    'DMin':"7A",
    'D#Min':"2A",
    'EMin':"9A",
    'FMin':"4A",
    'F#Min':"11A",
    'GMin':"6A",
    'G#Min':"1A",
    'AMin':"8A",
    'A#Min':"3A",
    'BMin':"10A"
}

worksheet = spreadsheet.get_worksheet(1) #Index of sheet, increment if you don't want to add to the current sheet

row_pointer=int(worksheet.get("B1")[0][0])
if row_pointer == 0:
    row_pointer = 2

print(row_pointer)


#playlist_url = 'http://open.spotify.com/playlist/0S0cuX8pnvmF7gA47Eu63M' #reddit.com/r/edm weekly playlist
#playlist_url = 'http://open.spotify.com/playlist/0xyqpMVkAmo6HNOpbZGMm2'
#playlist_url = 'https://open.spotify.com/playlist/7HubxREQJciZEOYY8CBi5D' #My Secret Sky Playlist
#playlist_url = 'https://open.spotify.com/playlist/3imvWy8mfgTiLfikvOav1x'
#playlist_url = 'https://open.spotify.com/playlist/4AjeQ7kRIx48DC6AivPySl'
playlist_url = 'https://open.spotify.com/playlist/37i9dQZF1DXa8NOEUWPn9W'

# Get the tracks from the playlist
results = sp.playlist_tracks(playlist_url)

# Loop through each track and print its key
for item in results['items']:
    track = item['track']
    track_name = track['name']
    artists = [artist['name'] for artist in track['artists']]
    
    # Get audio features for the track
    audio_features = sp.audio_features(track['id'])[0]

    # Extract the key and mode information and print it
    if audio_features and 'key' in audio_features and 'mode' in audio_features:
        key = audio_features['key']
        mode = audio_features['mode']
        musical_key = key_mapping.get(key, 'Unknown')
        key_mode = "Maj" if mode == 1 else "Min"
        full_key= str(key_mapping.get(key, 'Unknown'))+str(key_mode)

        # Current quota is 300/min
        # aka 5 per second
        worksheet.update('A'+str(row_pointer), str(track_name))

        worksheet.update('B'+str(row_pointer), str(artists)[1:-1])

        worksheet.update('C'+str(row_pointer), full_key)

        worksheet.update('D'+str(row_pointer), str(camelot_mapping.get(full_key, 'Unknown')))

        row_pointer += 1

        sleep(4)
        
worksheet.update('B1', str(row_pointer))



    

