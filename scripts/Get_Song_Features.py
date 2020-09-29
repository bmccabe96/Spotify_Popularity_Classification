import pandas as pd
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import sys
sys.path.insert(1, '/Users/brianmccabe/DataScience/Flatiron/mod3/Spotify/scripts/')
import config
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import requests
import numpy as np

# Create Spotify object
# Get credentials as stored in config file
cid = config.cid
secret = config.secret
username = config.username
scope = config.scope
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
redirect_uri = config.redirect_uri

# # Create Spotify object using above credentials
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
#
# # Create token for authentication
# token = util.prompt_for_user_token(username, scope, cid, secret, 'http://localhost:8080')
# if token:
#     sp = spotipy.Spotify(auth=token)
# else:
#     print("Can't get token for", username)

sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope,
                                       username=username)
token_info = sp_oauth.get_cached_token()
if not token_info:
    auth_url = sp_oauth.get_authorize_url(show_dialog=True)
    print(auth_url)
    response = input('Paste the above link into your browser, then paste the redirect url here: ')

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    token = token_info['access_token']
else:
    token = token_info['access_token']

sp = spotipy.Spotify(auth=token)


def refresh():
    global token_info, sp
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    token = token_info['access_token']
    sp = spotipy.Spotify(auth=token)


# Pull in song_ids from pickle, and then iterate throgh making calls to spotify and storing data in mysql
song_ids = pd.read_pickle("song_ids.pickle")
try:
    connection = mysql.connector.connect(host=config.host,
                                         user=config.user,
                                         port=config.port,
                                         password=config.password,
                                         database=config.database,
                                         auth_plugin='mysql_native_password')
    cursor = connection.cursor()
    use_query = "USE Spotify"
    cursor.execute(use_query)

    feature_bad_keys = ['type', 'id', 'uri', 'track_href', 'analysis_url']  # keys to ignore
    i = 11069  # creating this to make the function below have some form of verbose-ness
    # 11068's song id results in an error 404 -- something funky with that song id
    count = 0  # will refresh token every 100 calls
    for song in song_ids[11069:]:
        row = {'id': sp.track(song)['id']}
        for key, value in sp.audio_features(song)[0].items():
            if key not in feature_bad_keys:
                row[key] = value
        row['num_sections'] = len(sp.audio_analysis(song)['sections'])
        track = sp.track(song)
        row['explicit'] = 0 if track['explicit'] == False else 1
        row['song_name'] = track['name']

        row['popular'] = 0 if sp.track(song)['popularity'] < 50 else 1
        to_add = [row['id'], row['song_name'], row['danceability'], row['energy'], row['key'], row['loudness'],
                  row['mode'], row['speechiness'], row['acousticness'], row['instrumentalness'], row['liveness'],
                  row['valence'], row['tempo'], row['duration_ms'], row['time_signature'], row['num_sections'],
                  row['explicit'], row['popular']]

        insert_query = """
                        INSERT INTO Songs 
                        VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
        cursor.execute(insert_query, to_add)
        connection.commit()
        print(f"Added index {i} to database")
        i += 1

        if count == 25:
            refresh()
            count = 0

    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into Laptop table {}".format(error))

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
