from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from gui.main_screen import MainScreen
from gui.camera_screen import CameraScreen
from gui.upload_screen import ImageUploadScreen


# App Initialization
class ColorBlindApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(CameraScreen(name="camera"))
        sm.add_widget(ImageUploadScreen(name="image_upload"))

        return sm

if __name__ == "__main__":
    ColorBlindApp().run()
