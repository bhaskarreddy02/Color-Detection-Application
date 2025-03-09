from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
import cv2
from app.color_detection import get_closest_color

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        # Camera display
        self.image = Image()
        self.layout.add_widget(self.image)

        # Detected color display
        self.color_label = Button(text="Detecting Color...", font_size=20, size_hint=(1, 0.2))
        self.layout.add_widget(self.color_label)

        # Buttons for capture & resume
        self.button_layout = BoxLayout(size_hint=(1, 0.2))

        self.capture_button = Button(text="Capture / Freeze", font_size=20)
        self.capture_button.bind(on_press=self.capture_frame)
        self.button_layout.add_widget(self.capture_button)

        self.resume_button = Button(text="Resume Live Feed", font_size=20)
        self.resume_button.bind(on_press=self.resume_feed)
        self.button_layout.add_widget(self.resume_button)

        self.layout.add_widget(self.button_layout)

        # Back button
        self.back_button = Button(text="Back to Main", font_size=20, size_hint=(1, 0.2))
        self.back_button.bind(on_press=self.stop_camera)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

        # Capture control
        self.capture = None
        self.is_paused = False

    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        self.is_paused = False
        Clock.schedule_interval(self.update, 1.0 / 10)

    def update(self, dt):
        if self.is_paused:
            return  # Skip updating frame if paused

        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, -1)

            # Get the center pixel
            height, width, _ = frame.shape
            center_x, center_y = width // 2, height // 2
            b, g, r = frame[center_y, center_x]

            # Get the closest color name
            color_name = get_closest_color(r, g, b)
            self.color_label.text = f"Color: {color_name} ({r}, {g}, {b})"

            # Draw an indicator at the center
            cv2.circle(frame, (center_x, center_y), 10, (0, 255, 255), 2)

            # Convert frame to texture
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
            self.image.texture = texture

            # Keep a copy of the last frame if paused
            self.frozen_frame = frame.copy()

    def capture_frame(self, instance):
        # Pause live updates
        self.is_paused = True
        # print("Live feed paused! Frame captured.")

    def resume_feed(self, instance):
        # Resume live updates
        self.is_paused = False
        # print("Resuming live feed...")

    def stop_camera(self, instance):
        # Stop the camera updates and release the resource
        Clock.unschedule(self.update)
        if self.capture:
            self.capture.release()
        self.manager.current = "main"

    def on_leave(self):
        # Ensure resources are released properly when leaving the screen
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()

        Clock.unschedule(self.update)

