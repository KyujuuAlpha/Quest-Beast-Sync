import sys
import requests
import random
import time
import wget
import os.path

# URL constants
BSABER_API_BOOKMARKS_URL = "https://bsaber.com/wp-json/bsaber-api/songs/?bookmarked_by="
BSAVER_API_DOWNLOAD_URL = "https://api.beatsaver.com/download/key/"

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
    
def download_songs(songs):
    # move on to beat saver
    print("Downloading songs from BeatSaver..")

    # download the songs
    # for i in range(0, len(download_links)):
    #     # get current download stuff
    #     name = download_names[i]
    #     link = download_links[i]

    #     # download logic
    #     if link.find("beatsaver") != -1:
    #         if os.path.isfile(name + ".zip") == False:
    #             print("Downloading from: " + link)
    #             wget.download(link, name + ".zip")
    #             print()
    #             time.sleep(random.randint(1, 3))
    #         else:
    #             number_songs_zero = number_songs_zero + 1
    #             print("Song " + name + ".zip already downloaded, skipping..")
    #     else:
    #         number_songs_zero = number_songs_zero + 1
    #         print("Not a BeatSaver link, skipping song..")

    #     # timing logic
    #     time_spent = time_spent + (round(time.time() * 1000) - prev_time)
    #     prev_time = round(time.time() * 1000)

if __name__ == "__main__":
    bsaber_user = "enthri"
    songs, next_page = get_bsaber_songs(bsaber_user, 1)
    print(next_page)