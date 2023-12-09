import cv2 as cv

img_logo = cv.imread('opencv_data/opencv-logo.png')
img_logo = cv.resize(img_logo, [300, 356])

#Bild in Graustufen umwandeln
img_logo_gray = cv.cvtColor(img_logo, cv.COLOR_BGR2GRAY)

#Schwellwert anlegen
retcode, img_logo_th = cv.threshold(img_logo_gray, 50, 255, cv.THRESH_BINARY)

cv.imshow('img_logo', img_logo)
cv.imshow('img_logo_gray', img_logo_gray)
cv.imshow('img_logo_th', img_logo_th)
cv.waitKey(0)
cv.destroyAllWindows()
