from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture

import numpy as np
import cv2

from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty

class CameraViewWidget(BoxLayout):
	image_texture = ObjectProperty(None)
	cascade_file = "data/haarcascade_frontalface_alt2.xml"

	def __init__(self, **kwargs):
		super(CameraViewWidget, self).__init__(**kwargs)
		self.cap = cv2.VideoCapture(0)
		self.cascade = cv2.CascadeClassifier(self.cascade_file)
		print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		Clock.schedule_interval(self.captureImage, 1.0/50.0)

	def captureImage(self, dt):
		# ret:readの成否　frame：取得した画像
		ret, frame = self.cap.read()

		img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		face_list = self.cascade.detectMultiScale(img_gray, minSize=(100, 100))

        # 検出した顔に印を付ける
		for (x, y, w, h) in face_list:
			color = (0, 0, 225)
			pen_w = 3
			cv2.rectangle(frame, (x, y), (x+w, y+h), color, thickness = pen_w)

		# kivyのフォーマットに合わせる
		img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		img2 = cv2.flip(img2, 0)
		width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
		self.image_texture = Texture.create(size=(width, height))
		self.image_texture.blit_buffer(img2.tostring())