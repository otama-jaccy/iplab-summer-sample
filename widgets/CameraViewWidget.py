from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture

import numpy as np
import cv2

from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty

class CameraViewWidget(BoxLayout):
	image_texture = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(CameraViewWidget, self).__init__(**kwargs)
		#カメラの取得
		self.cap = cv2.VideoCapture(0)
		#関数の定期実行
		Clock.schedule_interval(self.captureImage, 1.0/50.0)

	def captureImage(self, dt):
		# ret:readの成否　frame：取得した画像
		ret, frame = self.cap.read()

		#グレースケールに変換
		img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		#opencvの画像をkivyのフォーマットに合わせる
		img2 = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
		img2 = cv2.flip(img2, 0)

		#カメラの解像度取得
		width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

		#描画
		self.image_texture = Texture.create(size=(width, height))
		self.image_texture.blit_buffer(img2.tostring())