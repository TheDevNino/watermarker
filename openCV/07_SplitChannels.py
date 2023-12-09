import cv2 as cv

img = cv.imread('opencv_data/baboon.jpg')
img = cv.resize(img, [256, 256])

B = img[:, :, 0]
G = img[:, :, 1]
R = img[:, :, 2]

outimg = cv.vconcat([B, G, R])

cv.imshow('img', img)
cv.imshow('outimg', outimg)
cv.waitKey(0)

