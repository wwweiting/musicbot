from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import pandas as pd
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    } 
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=TW"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_top_songs(token, song_id):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)
    return json_result



credentials_path = 'google.json'
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = pygsheets.authorize(service_file=credentials_path)


sheet_name = 'music'
worksheet = gc.open(sheet_name).sheet1


token = get_token()
result = search_for_artist(token, '') 
artist_id = result["id"]
artist_name = result["name"]
songs = get_songs_by_artist(token, artist_id)


data = []

for idx, song in enumerate(songs):
    song_id = song['id']
    top_song_info = get_top_songs(token, song_id)
    link = top_song_info["external_urls"]["spotify"]
    data.append({'music': song['name'], 'artist': artist_name, 'ID': song_id, 'link': link})

df = pd.DataFrame(data)
worksheet.append_table(df.values.tolist(), start='A1', end=None, dimension='ROWS', overwrite=False)
