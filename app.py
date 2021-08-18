from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

class MainScreen(MDScreen):
    def sync(self):
        self.status.text = "Pressed"

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return MainScreen()

MainApp().run()