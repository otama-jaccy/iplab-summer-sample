import cv2

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
    #kivyファイルの読み込み(cssの読み込みみたいなものです)
    Builder.load_file('kivy/main.kv')
    Builder.load_file('kivy/widgets.kv')

    #Applicationの実行
    MainApp().run()