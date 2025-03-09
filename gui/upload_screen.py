from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
import cv2

from app.color_detection import get_closest_color


class ImageUploadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # === Main Horizontal Layout ===
        self.main_layout = BoxLayout(orientation="horizontal")

        # === Left Panel (File chooser 30%) ===
        self.left_panel = BoxLayout(orientation="vertical", size_hint=(0.3, 1))

        self.file_chooser = FileChooserIconView(filters=["*.png", "*.jpg", "*.jpeg"])
        self.file_chooser.bind(on_submit=self.load_image)
        self.left_panel.add_widget(self.file_chooser)

        # === Right Panel (Image + Controls 70%) ===
        self.right_panel = BoxLayout(orientation="vertical", size_hint=(0.7, 1))

        # -- Top 80%: Image + Pointer overlay --
        self.image_display_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.8))

        # Image display
        self.image_widget = Image(fit_mode="contain")  # Best practice replacement
        self.image_display_layout.add_widget(self.image_widget)

        # Pointer overlay (Widget)
        self.pointer_canvas = Widget()
        self.image_display_layout.add_widget(self.pointer_canvas)

        # -- Bottom 20%: Color Label + Back Button --
        self.bottom_controls_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2), spacing=10, padding=10)

        self.color_label = Label(text="Tap on Image to Detect Color", font_size=18, size_hint=(0.7, 1))
        self.bottom_controls_layout.add_widget(self.color_label)

        self.back_button = Button(text="Back to Main", font_size=18, size_hint=(0.3, 1))
        self.back_button.bind(on_press=self.go_back)
        self.bottom_controls_layout.add_widget(self.back_button)

        # Add everything to the right panel
        self.right_panel.add_widget(self.image_display_layout)
        self.right_panel.add_widget(self.bottom_controls_layout)

        # === Combine Panels in Main Layout ===
        self.main_layout.add_widget(self.left_panel)
        self.main_layout.add_widget(self.right_panel)

        # Add to Screen
        self.add_widget(self.main_layout)

        # Internal State
        self.image_texture = None
        self.image_path = ""

    # === File loading + interaction ===
    def load_image(self, chooser, selection, touch):
        if selection:
            self.image_path = selection[0]
            self.image_widget.source = self.image_path
            self.image_widget.reload()
            self.image_widget.bind(on_touch_down=self.get_color_from_image)

    def get_color_from_image(self, instance, touch):
        if not self.image_path:
            return

        # Widget size/pos
        widget = self.image_widget
        widget_x, widget_y = widget.pos
        widget_width, widget_height = widget.size

        # Touch inside image?
        if not (widget_x <= touch.x <= widget_x + widget_width and widget_y <= touch.y <= widget_y + widget_height):
            return

        # Relative coords inside widget (normalized 0 to 1)
        relative_x = (touch.x - widget_x) / widget_width
        relative_y = (touch.y - widget_y) / widget_height

        # OpenCV image loading
        img = cv2.imread(self.image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_height, img_width, _ = img.shape

        # Convert normalized coords to image pixel coords
        pixel_x = int(relative_x * img_width)
        pixel_y = int((1 - relative_y) * img_height)  # Invert y-axis because OpenCV's origin is top-left

        if 0 <= pixel_x < img_width and 0 <= pixel_y < img_height:
            r, g, b = img[pixel_y, pixel_x]
            color_name = get_closest_color(r, g, b)
            self.color_label.text = f"Color: {color_name} ({r}, {g}, {b})"

            # Draw the pointer (visual feedback)
            self.draw_pointer(touch.x, touch.y)

    def draw_pointer(self, x, y):
        # Clear any previous pointers
        self.pointer_canvas.canvas.clear()

        with self.pointer_canvas.canvas:
            Color(1, 0, 0, 1)  # Red pointer (R, G, B, A)
            radius = 10
            Ellipse(pos=(x - radius / 2, y - radius / 2), size=(radius, radius))

    def go_back(self, instance):
        self.manager.current = "main"
