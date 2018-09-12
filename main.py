import cv2
import numpy as np
from PIL import Image

# kivy lib
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

#widgets
from widgets.CameraViewWidget import CameraViewWidget

class Main(BoxLayout):
    pass

class MainApp(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    Builder.load_file('kivy/main.kv')
    Builder.load_file('kivy/widgets.kv')
    MainApp().run()