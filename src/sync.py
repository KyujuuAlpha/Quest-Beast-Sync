import requests
import zipfile
import os
import json

# URL constants
BSABER_API_BOOKMARKS_URL = "https://bsaber.com/wp-json/bsaber-api/songs/?bookmarked_by="
BSAVER_API_DOWNLOAD_URL = "https://api.beatsaver.com/download/key/"

# Folder constants
CUSTOM_LEVEL_FOLDER = "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/"
CUSTOM_PLAYLIST_FOLDER = "/sdcard/ModData/com.beatgames.beatsaber/Mods/PlaylistManager/Playlists/"

# retrieve bookmarked songs for BeastSaber user for a specified page
def get_bsaber_songs(user, page):
    # build and send the bsaber GET request
    page_url = "" if page == 1 else ("&page=" + str(page))
    bsaber_request = requests.get(BSABER_API_BOOKMARKS_URL + user + page_url)

    # quick status code check
    if bsaber_request.status_code != requests.codes.ok:
        return None

    # extract the json
    bsaber_json = bsaber_request.json()

    # return the data
    return bsaber_json["songs"], bsaber_json["next_page"]

# verify if the custom levels/playlists paths exists or not
def safe_path_check():
    # levels
    if os.path.exists(CUSTOM_LEVEL_FOLDER) == False:
        # create folder(s) if it does not exist
        os.makedirs(CUSTOM_LEVEL_FOLDER)
    
    # playlists
    if os.path.exists(CUSTOM_PLAYLIST_FOLDER) == False:
        # create folder(s) if it does not exist
        os.makedirs(CUSTOM_PLAYLIST_FOLDER)

# download a single song from beatsaver, returns true if it downloads
def download_song(song):
    # construct the download url and download location
    song_url = BSAVER_API_DOWNLOAD_URL + song["song_key"]
    extract_location = CUSTOM_LEVEL_FOLDER + song["hash"]
    download_location = song["hash"] + ".zip"

    # basic check if it already exists or not
    if os.path.exists(extract_location) == False:
        # download the file (streaming)
        with requests.get(song_url, stream=True) as response:
            # write the file (in chunks)
            with open(download_location, "wb") as file:
                for data_chunk in response.iter_content(chunk_size=1024):
                    if data_chunk:
                        file.write(data_chunk)
        
        # extract the file
        with zipfile.ZipFile(download_location, "r") as zip_file:
            zip_file.extractall(extract_location)

        # remove the zip file
        os.remove(download_location)
    else:
        return False

# create a playlist for the given song list and user
def create_playlist(song_list, user):
    # construct the file location and data
    playlist_location = CUSTOM_PLAYLIST_FOLDER + user + "_bookmarks.json"
    playlist_data = {"playlistTitle": ("Bookmarks (" + user + ")"), "playlistAuthor": None, "playlistDescription": None,
                     "songs": song_list, "image": None}
    
    # write the file
    with open(playlist_location, "w") as playlist_file:
        json.dump(playlist_data, playlist_file)