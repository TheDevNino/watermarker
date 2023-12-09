import cv2
import numpy as np


class App:

    def __init__(self):
        self._img = np.zeros((400, 400, 3), dtype=np.uint8)
        cv2.namedWindow('MyWindow')
        cv2.setMouseCallback('MyWindow', self.on_mouse)
        cv2.imshow('MyWindow', self._img)
        self.createTrackbarRGB()
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord("s"):
                self.on_s()
        cv2.destroyAllWindows()
    def createTrackbarRGB(self):
        # Create window for trackbars
        cv2.namedWindow('RGB Trackbars', cv2.WINDOW_NORMAL)  # Adjusted window size
        # Create trackbars for each RGB channel
        cv2.createTrackbar('Blue', 'RGB Trackbars', 0, 255, self.on_trackbar_blue)
        cv2.createTrackbar('Green', 'RGB Trackbars', 0, 255, self.on_trackbar_green)
        cv2.createTrackbar('Red', 'RGB Trackbars', 0, 255, self.on_trackbar_red)

    def on_trackbar_blue(self, value):
        # Handle trackbar changes for blue channel
        self._img[:, :, 0] = value
        cv2.imshow('MyWindow', self._img)

    def on_trackbar_green(self, value):
        # Handle trackbar changes for green channel
        self._img[:, :, 1] = value
        cv2.imshow('MyWindow', self._img)

    def on_trackbar_red(self, value):
        # Handle trackbar changes for red channel
        self._img[:, :, 2] = value
        cv2.imshow('MyWindow', self._img)

    @staticmethod
    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('Left button clicked at ({}, {})'.format(x, y))

    def on_s(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self._img, 'OpenCV', (50, 150), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('MyWindow', self._img)


if __name__ == "__main__":
    app = App()
