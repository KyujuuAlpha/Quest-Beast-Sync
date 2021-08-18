import requests
import zipfile
import os


# URL constants
BSABER_API_BOOKMARKS_URL = "https://bsaber.com/wp-json/bsaber-api/songs/?bookmarked_by="
BSAVER_API_DOWNLOAD_URL = "https://api.beatsaver.com/download/key/"

# Folder constants
CUSTOM_LEVEL_FOLDER = "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/"

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

# verify if the custom levels path exists or not
def safe_path_check():
    if os.path.exists(CUSTOM_LEVEL_FOLDER) == False:
        # create folder(s) if it does not exist
        os.makedirs(CUSTOM_LEVEL_FOLDER)

# download a single song from beatsaver, returns true if it downloads
def download_song(song):
    # construct the download url and download location
    song_url = BSAVER_API_DOWNLOAD_URL + song["song_key"]
    extract_location = CUSTOM_LEVEL_FOLDER + song["hash"]
    download_location = song["hash"]  + ".zip"

    # basic check if it already exists or not
    if os.path.exists(extract_location) == False:
        # download the file
        print("downloading from: " + song_url)
        data = requests.get(song_url)
        with open(download_location, "wb") as file:
            file.write(data.content)
        
        print ("Extracting: " + download_location)
        # extract the file
        with zipfile.ZipFile(download_location, "r") as zip_file:
            zip_file.extractall(extract_location)

        # remove the zip file
        os.remove(download_location)
    else:
        print(extract_location + " already exists")
        return False