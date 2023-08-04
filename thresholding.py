import cv2
import numpy as np

def ThresholdBinaryImage(frame):
    # Step 1: Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Step 2: Color thresholding
    lower_color = np.array([0, 100, 100])  # Define your lower color range (in HSV)
    upper_color = np.array([30, 255, 255]) # Define your upper color range (in HSV)
    color_mask = cv2.inRange(hsv, lower_color, upper_color)

    # Step 3: Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 4: Gradient-based thresholding
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    gradient_magnitude = np.uint8(255 * gradient_magnitude / np.max(gradient_magnitude))

    # Step 5: Combine color thresholded and gradient thresholded images
    combined = np.zeros_like(color_mask)
    combined[(color_mask == 255) | (gradient_magnitude > 50)] = 255

    # Step 6: Apply a final binary threshold
    _, binary = cv2.threshold(combined, 1, 255, cv2.THRESH_BINARY)

    return binary

def create_mask(edges):
    # Get the dimensions (number of rows and columns) of the edges image
    rows, cols = edges.shape[:2]

    # Define the vertices of the polygon that represents the region of interest (ROI)
    vertices = np.array([
        (200, 720),  # bottom-left corner
        (556, 447),  # top-left corner
        (720, 447),  # top-right corner
        (1325, 720)  # bottom-right corner
    ], np.int32)

    # Create a single-channel mask with zeros (black)
    mask = np.zeros((rows, cols), dtype=np.uint8)

    # Fill the specified polygon with white color (255) in the mask
    cv2.fillPoly(mask, [vertices], 255)

    # Resize the mask to match the size of the edges image using nearest-neighbor interpolation
    mask = cv2.resize(mask, (cols, rows), interpolation=cv2.INTER_NEAREST)

    return mask