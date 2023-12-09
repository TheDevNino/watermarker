import cv2 as cv            # Library zur Bildbearbeitung / -verarbeitung
from pathlib import Path    # Library um Dateipfade zu prüfen
from image_processor import ImageProcessor

def check_file_path(file_path):
    return Path(file_path).is_file()

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

def run():
    main_image_path = get_user_input(
        "Gib den Dateipfad des Hauptbildes ein: ",
        "Fehler: Dateipfad existiert nicht. Bitte erneut eingeben."
    )

    logo_path = get_user_input(
        "Gib den Dateipfad des Logos ein: ",
        "Fehler: Dateipfad existiert nicht. Bitte erneut eingeben."
    )

    processor = ImageProcessor(main_image_path, logo_path)
    processor.resize_image(1000, 800)
    logo_height, logo_width = processor.get_logo_dimensions()

    while True:
        try:
            x_start = get_integer_input(
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
                processor.insert_logo(x_start, y_start)
                processor.show_image()
                print(processor.get_image_sizes())
                break
        except ValueError:
            print("Fehler: Bitte ganze Zahlen für die Koordinaten eingeben.")

if __name__ == '__main__':
    run()

# Test Files: "openCV/opencv_data/board.jpg", "openCV/opencv_data/opencv-logo.png"