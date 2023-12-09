import cv2 as cv

img1 = cv.imread('opencv_data/ml.png')
Height, Width, Channels = img1.shape

img_logo = cv.imread('opencv_data/opencv-logo.png')
img2 = cv.resize(img_logo, (Width, Height))

dst = cv.addWeighted(img1, 0.7, img2, 0.3, 0)
cv.imshow('img1', img1)
cv.imshow('img2', img2)
cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()
