import cv2 as cv

class ImageProcessor:
    def __init__(self, main_image_path, logo_path):
        self.main_image = cv.imread(main_image_path)            # Hauptbild laden
        self.logo = cv.imread(logo_path)                        # Logo laden
        self.logo_height, self.logo_width, _ = self.logo.shape  # Höhe und Breite des Logos erhalten

    def get_logo_dimensions(self):
        return self.logo_height, self.logo_width # Logo-Dimensionen zurückgeben

    def resize_image(self, width, height):
        self.main_image = cv.resize(self.main_image, (width, height))  # Bildgröße ändern

    def add_alpha_channel(self):
        gray = cv.cvtColor(self.logo, cv.COLOR_BGR2GRAY)  # Logo in Graustufen konvertieren
        ret, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)  # Schwellenwert anwenden
        alpha = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)  # Alphakanal hinzufügen
        return alpha

    def insert_logo(self, x_start, y_start):
        x_end = x_start + self.logo_width  # X-Ende des Bildausschnitts berechnen
        y_end = y_start + self.logo_height  # Y-Ende des Bildausschnitts berechnen

        patch = self.main_image[y_start:y_end, x_start:x_end, :]  # Bildausschnitt erhalten
        alpha = self.add_alpha_channel()  # Alphakanal hinzufügen

        # Ausgabe der Dimensionen für Diagnosezwecke
        print("Alphakanal-Größe:", alpha.shape)
        print("Bildausschnitt-Größe:", patch.shape)

        patch[alpha > 0] = 0  # Alpha-Overlay auf den Bildausschnitt anwenden
        patch += self.logo  # Logo in den Bildausschnitt einfügen
        self.main_image[y_start:y_end, x_start:x_end, :] = patch  # Bildausschnitt mit Logo aktualisieren

    def show_image(self):
        cv.imshow("Patched Image", self.main_image)  # Bild anzeigen
        cv.waitKey(0)  # Warten, bis eine Taste gedrückt wird
        cv.destroyAllWindows()  # Alle Fenster schließen

    def get_image_sizes(self):
        return {
            "Logo-Größe": self.logo.shape,
            "Bild-Größe": self.main_image.shape
        }  # Größeninformationen zurückgeben


def check_patch_dimensions(main_image, logo, x_start, y_start):
    logo_height, logo_width, _ = logo.shape
    x_end = x_start + logo_width
    y_end = y_start + logo_height

    # Überprüfen, ob der Bildausschnitt innerhalb der Grenzen des Hauptbildes liegt
    if x_end > main_image.shape[1] or y_end > main_image.shape[0]:
        return False  # Dimensionen passen nicht zur Logo-Größe
    return True  # Dimensionen passen zur Logo-Größe


# Verwendung der Klasse
processor = ImageProcessor("openCV/opencv_data/board.jpg", "openCV/opencv_data/opencv-logo.png")
processor.resize_image(1000, 800)
logo_height, logo_width = processor.get_logo_dimensions()
x_start = 0
y_start = 0

# Überprüfung der Bildausschnittsdimensionen
if check_patch_dimensions(processor.main_image, processor.logo, x_start, y_start):
    processor.insert_logo(x_start, y_start)
    processor.show_image()
    print(processor.get_image_sizes())
else:
    print("Fehler: Bildausschnittsdimensionen passen nicht zur Logo-Größe.")
