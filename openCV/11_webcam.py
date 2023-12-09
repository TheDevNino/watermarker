import cv2
import numpy as np

def load_watermark():
    watermark = cv2.imread("opencv_data/logo.png", cv2.IMREAD_UNCHANGED)
    (B, G, R, A) = cv2.split(watermark)
    B = cv2.bitwise_and(B, B, mask=A)
    G = cv2.bitwise_and(G, G, mask=A)
    R = cv2.bitwise_and(R, R, mask=A)
    watermark = cv2.merge([B, G, R, A])
    return watermark

def add_watermark(img, watermark):
    scale_percent = 20  # percent of original size
    width = int(watermark.shape[1] * scale_percent / 100)
    height = int(watermark.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    watermark = cv2.resize(watermark, dim, interpolation=cv2.INTER_AREA)


    # get dimensions
    (wH, wW) = watermark.shape[:2]
    (h, w) = img.shape[:2]
    # add dummy alpha
    image = np.dstack([img, np.ones((h, w), dtype="uint8") * 255])
    # construct an overlay that is the same size as the input
    # image, (using an extra dimension for the alpha transparency),
    # then add the watermark to the overlay in the bottom-right
    # corner
    overlay = np.zeros((h, w, 4), dtype="uint8")
    overlay[0:wH, w - wW - 10:w - 10] = watermark
    # blend the two images together using transparent overlays
    output = image.copy()
    cv2.addWeighted(overlay, 0.5, output, 1.0, 0, output)
    return output


# Load the pre-trained Haarcascades face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open a connection to the webcam (usually 0 for the default webcam)
cap = cv2.VideoCapture(0)

# Variable to keep track of whether to mirror the frame
mirror_frame = False
wm_enabled = True
watermark = load_watermark()



while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Mirror the frame horizontally if needed
    if mirror_frame:
        frame = cv2.flip(frame, 1)

    if wm_enabled:
        frame = add_watermark(img=frame, watermark=watermark)

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame with detected faces
    cv2.imshow('Face Detection', frame)

    # Check for key press to toggle mirror effect
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):  # Toggle mirror effect on space key press
        mirror_frame = not mirror_frame
    elif key == ord('w'):  # Toggle mirror effect on space key press
        wm_enabled = not wm_enabled

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
