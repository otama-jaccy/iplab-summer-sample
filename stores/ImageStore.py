from threading import Lock
from utils.Singleton import Singleton
import cv2 as cv

class ImageStore(Singleton):
    def __init__(self):
        self._image = None
        self._image_lock = Lock()

    def update_image(self, image):
        with self.image_lock:
            self.image = cv.copy(image)

    def get_image(self):
        with self._image_lock:
            return cv.copy(self.image)