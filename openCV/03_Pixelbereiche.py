import cv2 as cv

img = cv.imread('opencv_data/messi5.jpg')
print(type(img))

TLXY = [332, 287]
BRXY = [391, 338]
offsetX = -200
offsetY = -5

#Auswahl und "Ball-Bild" in Variable ball speichern
ball = img[TLXY[1]:BRXY[1], TLXY[0]:BRXY[0], :]

#An anderer Stelle wieder einfügen
img[TLXY[1]+offsetY:BRXY[1]+offsetY, TLXY[0]+offsetX:BRXY[0]+offsetX, :] = ball

cv.imshow("Display window", img)
k = cv.waitKey(0)

