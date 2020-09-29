import pandas as pd
import config
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pickle

# Get credentials as stored in config file
cid = config.cid
secret = config.secret
username = config.username
scope = config.scope

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

# Create Spotify object using above credentials
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create token for authentication
token = util.prompt_for_user_token(username, scope, cid, secret, 'http://localhost:8080')
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

# Pull in albums from pickled file
# (<album_name>, <album_date>)
albums = pd.read_pickle("albums_2015_to_2020.pickle")

# Create a list of song ids by search each album in spotify.
# Verify that we are searching the right album my cross referencing thr date
song_ids = []
count = 0
for album in albums:
    for track in sp.search(album[0])['tracks']['items']:
        if track['album']['name'] == album[0] and track['album']['release_date'][:4] == str(album[1]):
            song_ids.append(track['id'])

# Pickle the file for later use
pickle_out = open("song_ids.pickle", "wb")
pickle.dump(song_ids, pickle_out)
pickle_out.close()
