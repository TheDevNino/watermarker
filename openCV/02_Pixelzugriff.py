import cv2 as cv

img = cv.imread('opencv_data/messi5.jpg')

bgrvalue = img[162, 218, :] #Position des roten Streifens auf dem Trickot
print(bgrvalue)

