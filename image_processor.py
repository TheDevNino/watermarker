import cv2 as cv
import numpy as np

class ImageProcessor:
    def __init__(self, main_image_path, logo_path, text_input):
        self.main_image = cv.imread(main_image_path)            # Hauptbild laden
        self.main_image_height, self.main_image_width, _ = self.main_image.shape

        if text_input == "":
            self.logo = cv.imread(logo_path)                        # Logo laden
            self.logo_height, self.logo_width, _ = self.logo.shape  # Höhe und Breite des Logos erhalten

        if logo_path == "":
            self.text = text_input

    # Funktionen der Klasse
    def get_main_image_dimensions(self):
        return self.main_image_height, self.main_image_width # Dimensionen zurückgeben
    def get_logo_dimensions(self):
        return self.logo_height, self.logo_width # Logo-Dimensionen zurückgeben

    def resize_logo(self, width, height):
        self.logo = cv.resize(self.logo, (width, height))  # Bildgröße ändern
    def resize_image(self, width, height):
        self.main_image = cv.resize(self.main_image, (width, height))  # Bildgröße ändern

    def add_alpha_channel(self):
        gray = cv.cvtColor(self.logo, cv.COLOR_BGR2GRAY)  # Logo in Graustufen konvertieren
        ret, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)  # Schwellenwert anwenden
        alpha = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)  # Alphakanal hinzufügen
        return alpha

    def insert_logo(self, x_start, y_start):
        x_end = x_start + self.logo_width
        y_end = y_start + self.logo_height
        patch = self.main_image[y_start:y_end, x_start:x_end, :]

        alpha = self.add_alpha_channel()
        mask = alpha[:, :, 0] > 0

        # Normalisiere den Alphakanal auf den Bereich [0, 1]
        normalized_alpha = alpha[:, :, 0] / 255.0

        alpha = 0.8
        beta = 0.2
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

    def get_image_sizes(self):
        return {
            "Logo-Größe": self.logo.shape,
            "Bild-Größe": self.main_image.shape
        }  # Größeninformationen zurückgeben

    def set_logo_opacity(self, alpha_value):
        # ...
        return