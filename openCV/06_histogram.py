import cv2 as cv
import matplotlib.pyplot as plt


img_logo = cv.imread('opencv_data/opencv-logo.png')
img_logo_gray = cv.cvtColor(img_logo, cv.COLOR_BGR2GRAY)

#Figure erstellen
plt.figure(figsize=(5, 3))

#Histogramm berechnen und anzeigen
plt.hist(img_logo_gray.flatten(), 100, density=True)

#Plotgestaltung
plt.title("Histogram von img_logo_gray")
plt.xlabel("Grauwert (0-255)")
plt.ylabel("Relative Häufigkeit")
plt.axvline(50, color='r', ls='--', alpha=.5)
plt.grid()
plt.tight_layout()
plt.show()
