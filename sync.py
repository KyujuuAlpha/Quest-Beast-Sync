import sys
import requests
import random
import time
import wget
import os.path

# URL constants
BSABER_API_BOOKMARKS_URL = "https://bsaber.com/wp-json/bsaber-api/songs/?bookmarked_by="
BSAVER_API_DOWNLOAD_URL = "https://api.beatsaver.com/download/key/"

# Folder constants
# CUSTOM_LEVEL_FOLDER = "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels"
CUSTOM_LEVEL_FOLDER = "./CustomLevels"

# retrieve bookmarked songs for BeastSaber user for a specified page
# {"title":"Darling Dance(YuNi Cover) - Kairiki Bear","song_key":"1b49e","hash":"57431519f148298175a53720b68907a6f4a52456","level_author_name":"Emir"}
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

if __name__ == "__main__":
    bsaber_user = "enthri"
    
    if os.path.exists(CUSTOM_LEVEL_FOLDER) == False:
        print("Folder does not exist, creating..")
        os.mkdir(CUSTOM_LEVEL_FOLDER)
    
    songs, next_page = get_bsaber_songs(bsaber_user, 1)
    if songs != None:
        for song in songs:
            song_url = BSAVER_API_DOWNLOAD_URL + song["song_key"]
            download_location = CUSTOM_LEVEL_FOLDER + "/" + song["hash"] + ".zip"
            if os.path.exists(download_location) == False:
                wget.download(song_url, download_location)
            else:
                print("Song exists..")
    else:
        print("Songs not found!")
        exit(1)
    print(next_page)