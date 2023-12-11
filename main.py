import cv2 as cv            # Library zur Bildbearbeitung / -verarbeitung
from pathlib import Path    # Library um Dateipfade zu prüfen
from image_processor import ImageProcessor
import numpy as np

def check_patch_dimensions(main_image, logo, x_start, y_start):
    logo_height, logo_width, _ = logo.shape
    x_end = x_start + logo_width
    y_end = y_start + logo_height
    return x_end <= main_image.shape[1] and y_end <= main_image.shape[0]

def get_user_input(message, error_message):
    while True:
        user_input = input(message)
        if not check_file_path(user_input):
            print(error_message)
        else:
            return user_input

def get_integer_input(message, error_message):
    while True:
        user_input = input(message)
        if not user_input.isdigit():
            print(error_message)
        else:
            return int(user_input)

def get_max_scale_factor(logoX, logoY, imgX, imgY):
    scaling_factor_width = imgX / logoX
    scaling_factor_height = imgY / logoY
    scaling_factor = min(scaling_factor_width, scaling_factor_height)
    return round(scaling_factor-0.01, 2) # Rundung - Verhinderung Rundungsfehler

def resize_images(processor):
    print(processor.get_image_sizes())
    msf = get_max_scale_factor(processor.logo_width,processor.logo_height,processor.main_image_width,processor.main_image_height)
    while True:
        scale_factor = float(
            input(f"Gib den Skalierungsfaktor für das Logo ein (max. {msf}): "))
        if scale_factor <= msf:
            break
        else:
            print(f"Der eingegebene Skalierungsfaktor ist zu groß. Bitte gib einen Wert kleiner oder gleich {msf} ein.")
    Xresized_logo = int(processor.logo_width * scale_factor)
    Yresized_loog = int(processor.logo_height * scale_factor)
    processor.resize_logo(Xresized_logo, Yresized_loog)

    print(processor.get_image_sizes())

def check_file_path(file_path):
    return Path(file_path).is_file()

def create_image_instances(needLogo):
    main_image_path = get_user_input(
        "Gib den Dateipfad des Hauptbildes ein: ",
        "Fehler: Dateipfad existiert nicht. Bitte erneut eingeben."
    )
    if needLogo:
        logo_path = get_user_input(
            "Gib den Dateipfad des Logos ein: ",
            "Fehler: Dateipfad existiert nicht. Bitte erneut eingeben."
        )
        text_input = ""
    else:
        logo_path = ""
        text_input = input("Gib den Wasserzeichen-Text ein: ")
    return ImageProcessor(main_image_path, logo_path, text_input)

def position_logo(processor):
    while True:
        try:
            x_start = get_integer_input(                                        #### Noch maximalwerte anzeigen lassen
                "Gib die X-Startkoordinate für das Logo ein: ",
                "Fehler: Bitte ganze Zahlen für die Koordinaten eingeben."
            )
            y_start = get_integer_input(
                "Gib die Y-Startkoordinate für das Logo ein: ",
                "Fehler: Bitte ganze Zahlen für die Koordinaten eingeben."
            )
            if not check_patch_dimensions(processor.main_image, processor.logo, x_start, y_start):
                print("Fehler: Bildausschnittsdimensionen passen nicht zur Logo-Größe.")
            else:
                break
        except ValueError:
            print("Fehler: Bitte ganze Zahlen für die Koordinaten eingeben.")
    return x_start, y_start

def addLogo(processor, x_start, y_start):
    processor.insert_logo(x_start, y_start)
    print(processor.get_image_sizes())

def addText(processor):
    font = cv.FONT_HERSHEY_SIMPLEX
    x_start = get_integer_input(  #### Noch maximalwerte anzeigen lassen
        "Gib die X-Startkoordinate für das Logo ein: ",
        "Fehler: Bitte ganze Zahlen für die Koordinaten eingeben."
    )
    y_start = get_integer_input(
        "Gib die Y-Startkoordinate für das Logo ein: ",
        "Fehler: Bitte ganze Zahlen für die Koordinaten eingeben."
    )
    fontScale = get_integer_input("Skalierung: ", "Falsche Eingabe.")
    while True:
        color_input = input("Farbe: Rot (r), Grün (g), Blau (b), Weiss (w), Schwarz (s)")
        if color_input == "r":
            fontColor = (0, 0, 255)
            break
        elif color_input == "g":
            fontColor = (0, 255, 0)
            break
        elif color_input == "b":
            fontColor = (255, 0, 0)
            break
        elif color_input == "w":
            fontColor = (255, 255, 255)
            break
        elif color_input == "s":
            fontColor = (0, 0, 0)
            break
        else:
            print("Ungültige Eingabe. Wähle eine der vorgegebenen Farben.")

    while True:
        opacity = float(input("Wählen sie einen Wert für die Transparenz des Logos (zwischen 0.0 und 1.0): "))
        if opacity <= 1.0 and opacity >= 0.0:
            break
        else:
            print("Der Wert muss zwischen 0.0 und 1.0 liegen.")

    overlay = np.zeros_like(processor.main_image, dtype=np.uint8)

    thickness = 5
    lineType = 2

    textSize = cv.getTextSize(
        processor.text,
        font,
        fontScale,
        thickness
    )
    #print("Size:",textSize)

    topRightCornerOfText = (x_start, y_start+int(textSize[0][1]))

    cv.putText(overlay,
                processor.text,
               topRightCornerOfText,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    cv.addWeighted(overlay, opacity, processor.main_image, 1 - opacity, 0, processor.main_image)


def run():
    while True:
        type_request = input("Bild-Logo (b) oder Text-Logo (t) verwenden? ")
        if type_request == "b":
            needLogo = True
            break
        elif type_request == "t":
            needLogo = False
            break
        else:
            print("Eingabe Ungültig. Versuche es erneut.")
    processor = create_image_instances(needLogo)
    if needLogo:
        resize_images(processor)
        x, y = position_logo(processor)

        addLogo(processor, x, y)
    else:
        addText(processor)
    processor.show_image()

if __name__ == '__main__':
    run()

'''
Test Files:
openCV/opencv_data/board.jpg
openCV/opencv_data/opencv-logo.png
openCV/opencv_data/WindowsLogo.jpg
openCV/opencv_data/LinuxLogo.jpg
'''