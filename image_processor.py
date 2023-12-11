import cv2 as cv
import numpy as np
import os

class ImageProcessor:
    def __init__(self, main_image_path, logo_path, text_input):
        self.main_image = cv.imread(main_image_path)            # Hauptbild laden
        self.main_image_height, self.main_image_width, _ = self.main_image.shape

        if text_input == "":
            self.logo = cv.imread(logo_path)                        # Logo laden
            self.set_logo_dimensions()

        if logo_path == "":
            self.text = text_input

    # Funktionen der Klasse
    def get_main_image_dimensions(self):
        return self.main_image_height, self.main_image_width # Dimensionen zurückgeben
    def set_logo_dimensions(self):
        self.logo_height, self.logo_width, _ = self.logo.shape

    def resize_logo(self, width, height):
        self.logo = cv.resize(self.logo, (width, height))  # Bildgröße ändern
        self.set_logo_dimensions()

    def add_alpha_channel(self):
        gray = cv.cvtColor(self.logo, cv.COLOR_BGR2GRAY)  # Logo in Graustufen konvertieren
        ret, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)  # Schwellenwert anwenden
        alpha = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)  # Alphakanal hinzufügen
        return alpha

    def insert_logo(self, x_start, y_start):
        x_end = x_start + self.logo_width
        y_end = y_start + self.logo_height
        print(x_end, y_end)
        patch = self.main_image[y_start:y_end, x_start:x_end, :]

        alpha_channel = self.add_alpha_channel()
        mask = alpha_channel[:, :, 0] > 0

        # Normalisiere den Alphakanal auf den Bereich [0, 1]
        normalized_alpha = alpha_channel[:, :, 0] / 255.0

        # Benutzereingabe für alpha
        while True:
            alpha = float(input("Wählen sie einen Wert für die Transparenz des Logos (zwischen 0.0 und 1.0): "))
            if alpha <= 1.0 and alpha >= 0.0:
                break
            else:
                print("Der Wert muss zwischen 0.0 und 1.0 liegen.")

        # Setze den Wert für beta als 1 - alpha
        beta = 1 - alpha

        print(patch.shape, self.logo.shape)

        dst = cv.addWeighted(self.logo.astype(np.uint8), alpha, patch.astype(np.uint8), beta, 0.0)

        # Setze die Pixel im Patch, die transparent sind, auf Schwarz
        patch[mask] = 0

        # Skaliere dst um den normalisierten Alphakanal
        dst = (dst * normalized_alpha[:, :, np.newaxis]).astype(np.uint8)

        patch += dst

        self.main_image[y_start:y_end, x_start:x_end, :] = patch

    def show_image(self):
        cv.imshow("Patched Image", self.main_image)  # Bild anzeigen
        cv.waitKey(0)  # Warten, bis eine Taste gedrückt wird
        cv.destroyAllWindows()  # Alle Fenster schließen

    def save_image(self):
        # Filename
        while True:
            filename = input("Gib einen Dateinamen zum Abspeichern ein: ")
            if len(filename) > 255:
                print("Der Dateiname überschreitet die maximale Länge.")
            else:
                # Überprüfe die Existenz und Schreibbarkeit der Datei
                if os.path.exists(filename):
                    print("Die Datei existiert bereits.")
                else:
                    break

        cv.imwrite(filename, self.main_image)

    def get_image_sizes(self):
        return {
            "Logo-Größe": self.logo.shape,
            "Bild-Größe": self.main_image.shape
        }  # Größeninformationen zurückgeben
