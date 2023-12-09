import cv2 as cv
import numpy as np

def load_logo(height, width):
    img_logo = cv.imread('opencv_data/opencv-logo.png')
    image_with_alpha = cv.imread("opencv_data/opencv-logo.png", cv.IMREAD_UNCHANGED)
    # Alpha auswählen
    alpha = image_with_alpha[:, :, 3]
    # Logo auf Schwarz setzen wo alpha = 0 (transparent)
    img_logo[alpha == 0] = 0
    # Alpha Kanal abschneiden
    img_logo = img_logo[:, :, :3]
    # Logo auf definierte Größe setzen
    img_logo = cv.resize(img_logo, [height, width])
    return img_logo


def get_threshold(img):
    #Bild in Graustufen umwandeln
    img_logo_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #Schwellwert anlegen
    retcode, img_logo_th = cv.threshold(img_logo_gray, 20, 255, cv.THRESH_BINARY)

    img_logo_th = cv.cvtColor(img_logo_th, cv.COLOR_GRAY2BGR)
    return img_logo_th


def use_patch(img, img_logo, img_logo_th):
    LogoHeight, LogoWidth, _ = img_logo.shape
    # Patch erstellen
    patch = img[0:LogoHeight, 0:LogoWidth, :]
    # Patch auf Schwarz setzen für Logo
    patch[img_logo_th > 0] = 0
    # Logo in den Patch schreiben (muss gleich groß sein)
    patch += img_logo


def adding(img, img_logo):
    imgHeight, imgWidth, _ = img.shape
    LogoHeight, LogoWidth, _ = img_logo.shape
    # Leeres Bild erstellen
    canvas = np.zeros((imgHeight, imgWidth, 3), np.uint8)
    # Logomaße oben links ausschneiden und überschreiben
    canvas[0:LogoHeight, 0:LogoWidth, :] = img_logo
    # Logo in das Bild schreiben mit 0.7 alpha und img 1
    result = cv.addWeighted(canvas, 0.8, img, 1, 0)
    return result


def main():
    img_logo = load_logo(150, 150)
    img = cv.imread('opencv_data/messi5.jpg')

    img_logo_th = get_threshold(img_logo)
    #use_patch(img, img_logo, img_logo_th)
    img = adding(img, img_logo)
    cv.imshow('img', img)
    cv.waitKey(0)


if __name__ == "__main__":
    main()
