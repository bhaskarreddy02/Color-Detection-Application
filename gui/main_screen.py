from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        # Buttons
        camera_button = Button(text="Live Camera Mode", font_size=20, size_hint=(1, 0.3))
        camera_button.bind(on_press=self.go_to_camera)

        image_button = Button(text="Upload Image Mode", font_size=20, size_hint=(1, 0.3))
        image_button.bind(on_press=self.go_to_image_upload)

        exit_button = Button(text="Exit", font_size=20, size_hint=(1, 0.3))
        exit_button.bind(on_press=self.exit_app)

        layout.add_widget(camera_button)
        layout.add_widget(image_button)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def go_to_camera(self, instance):
        self.manager.current = "camera"

    def go_to_image_upload(self, instance):
        self.manager.current = "image_upload"

    def exit_app(self, instance):
        App.get_running_app().stop()

