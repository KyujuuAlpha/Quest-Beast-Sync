from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.clock import mainthread
from android.permissions import Permission, request_permissions

import sync
import threading

# main root widget
class MainScreen(MDScreen):
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

    def download_thread(self):
        # check if path exists
        sync.safe_path_check()

        # retrieve user
        bsaber_user = self.user.text

        # logic for one page
        self.set_status_text("Retrieving downloads from BeastSaber page 1")

        # retrieve songs from bsaber
        songs, next_page = sync.get_bsaber_songs(bsaber_user, 1)
        num_songs = len(songs)

        # if there are songs, then download and extract them
        if songs != None and num_songs > 0:
            for i in range(0, num_songs):
                self.set_status_text("Downloading song " + str(i + 1) + " of " + str(num_songs))
                song = songs[i]
                try:
                    sync.download_song(song)
                except Exception as err:
                    self.set_status_text("uh oh")

            self.set_status_text("Songs synchronized!")
        else:
            self.set_status_text("User has no bookmarked songs!")

        self.set_in_progress(False)

    # called when the synchronize button is pressed
    def sync(self):
        if len(self.user.text) == 0:
            self.set_status_text("Please enter BeastSaber username!")
            return
        
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