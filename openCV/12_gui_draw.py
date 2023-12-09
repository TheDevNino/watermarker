import cv2
import numpy as np

drawing = False
ix, iy = -1, -1

def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(img, (ix, iy), (x, y), (0, 0, 255), 5)
            ix, iy = x, y


img = np.zeros((500, 500, 3), dtype=np.uint8)
cv2.namedWindow('MyWindow')
cv2.setMouseCallback('MyWindow', draw_circle)

while True:
    cv2.imshow('MyWindow', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()
