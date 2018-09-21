from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture

import cv2
import numpy as np
from threading import Lock
from datetime import datetime

from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty

class CameraViewWidget(BoxLayout):
	#kivyの画像描画用テクスチャ
	image_texture = ObjectProperty(None)
	#画像を保存するか
	_is_saving = False
	#画像処理モード
	_state = 0 
	#カメラ
	_cap = cv2.VideoCapture(0)
	#カスケードファイルのパス
	_cascade = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")

	def __init__(self, **kwargs):
		super(CameraViewWidget, self).__init__(**kwargs)
		#スレッドセーフ用
		self._lock = Lock()
		#関数の定期実行
		Clock.schedule_interval(self.capture_image, 1.0/50.0)

	#グレースケール変換
	def convert_gray_scale(self, frame):
		return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	def save(self, img):
		cv2.imwrite('used_img/{0}.png'.format(datetime.now().strftime('%y%m%d%H%M%S%f')), img)

	#フィルター処理
	def filter(self, frame):
		filter_arr = np.array([
			[1, 1, 1],
			[1, -8, 1],
			[1, 1, 1]
		], np.float32)
		return cv2.filter2D(frame, cv2.CV_8U, filter_arr)

	#カスケード分類器による認識
	def cascade(self, frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		face = self._cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
		for (x, y, w, h) in face:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,200), 3)
		return frame

	#オリジナルの画像認識
	def recognize(self, frame):
		return frame

	def capture_image(self, dt):
		#画像処理の種類
		with self._lock:
			next_state = self._state
		
		# ret:readの成否　frame：取得した画像
		ret, frame = self._cap.read()
		# 取得画像の保存
		if self._is_saving:
			self.save(frame)

		# モードで画像処理を切り替え
		if next_state == 0:
			frame = self.filter(frame)
			color_format = cv2.COLOR_BGR2RGB
		elif next_state == 1:
			frame = self.convert_gray_scale(frame)
			color_format = cv2.COLOR_GRAY2RGB
		elif next_state == 2:
			frame = self.cascade(frame)
			color_format = cv2.COLOR_BGR2RGB
		else:
			frame = self.recognize(frame)
			color_format = cv2.COLOR_BGR2RGB

		#opencvの画像をkivyのフォーマットに合わせる
		disp_img = cv2.cvtColor(frame, color_format)
		disp_img = cv2.flip(disp_img, 0)

		#カメラの解像度取得
		width = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

		#描画
		self.image_texture = Texture.create(size=(width, height))
		self.image_texture.blit_buffer(disp_img.tostring())

	def on_press_save_button(self, _is_saving):
		self._is_saving = _is_saving

	#画像処理モードの変換
	def onChange(self, value):
		with self._lock:
			self._state = value