from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.clock import mainthread
from kivy.properties import NumericProperty
from android.permissions import Permission, request_permissions

import sync
import threading
import math
import time

DOWNLOAD_THREAD_COUNT = 6
THREAD_SPAWN_DELAY = 1

# main root widget
class MainScreen(MDScreen):

    download_counter = 0
    download_max = 0

    @mainthread
    def set_in_progress(self, disabled):
        # lock the ui according to the disabled parameter
        self.user.disabled = disabled
        self.button.disabled = disabled
        self.spinner.active = disabled
    
    @mainthread
    def set_status_text(self, text):
        # set the status of the downloading
        self.status.text = text

    @mainthread
    def status_counter_increase(self):
        self.download_counter += 1
        self.status.text = "Downloaded " + str(self.download_counter) + " of " + str(self.download_max)
    
    @mainthread
    def status_counter_reset(self, max):
        self.download_counter = 0
        self.download_max = max
        self.status.text = "Downloaded " + str(self.download_counter) + " of " + str(self.download_max)
    
    def song_download_worker(self, songs):
        for song in songs:
            sync.download_song(song)
            self.status_counter_increase()

    def download_thread(self):
        # retrieve user
        bsaber_user = self.user.text

        # logic for one page
        self.set_status_text("Retrieving downloads from BeastSaber page 1")

        # retrieve songs from bsaber
        songs, next_page = sync.get_bsaber_songs(bsaber_user, 1)
        num_songs = len(songs)

        # if there are songs, then download and extract them
        if songs != None and num_songs > 0:
            threads = []
            self.status_counter_reset(num_songs)
            if num_songs >= DOWNLOAD_THREAD_COUNT:
                chunk_size = math.floor(num_songs / DOWNLOAD_THREAD_COUNT)
                for i in range(0, DOWNLOAD_THREAD_COUNT):
                    worker_song_list = []
                    if i == DOWNLOAD_THREAD_COUNT - 1:
                        worker_song_list = songs[(chunk_size * i):]
                    else:
                        worker_song_list = songs[(chunk_size * i):(chunk_size * (i + 1))]
                    threads.append(threading.Thread(target = (self.song_download_worker), args=[worker_song_list]))
                    threads[-1].start()
                    time.sleep(THREAD_SPAWN_DELAY)
            else:
                threads.append(threading.Thread(target = (self.song_download_worker), args=[songs]))
                threads[-1].start()
            
            for thread in threads:
                thread.join()

            self.set_status_text("Songs synchronized!")
        else:
            self.set_status_text("User has no bookmarked songs!")

        self.set_in_progress(False)

    # called when the synchronize button is pressed
    def sync(self):
        if len(self.user.text) == 0:
            self.set_status_text("Please enter BeastSaber username!")
            return
        
        # check if path exists
        sync.safe_path_check()
        
        self.set_in_progress(True)
        threading.Thread(target = (self.download_thread)).start()

    # called when the exit button is pressed
    def exit(self):
        exit()

# the main application construction
class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return MainScreen()

if __name__ == "__main__":
    # make sure permissions are satisfied
    request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    # run the app
    MainApp().run()