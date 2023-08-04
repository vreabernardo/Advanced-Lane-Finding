import cv2
import numpy as np


def create_perspective_transform(frame, inverse=False):
    """
    Create a perspective transform for lane detection.

    Parameters:
        frame (numpy.ndarray): Input frame.

    Returns:
        numpy.ndarray: Perspective-transformed frame.
    """
    # Get the dimensions (number of rows and columns) of the input frame
    rows, cols = frame.shape[:2]

    # Define four points in the input frame representing the region of interest (ROI)
    # The ROI is a trapezoidal shape that we want to transform to a bird's-eye view
    pts1 = np.array([
        (200, 720),  # bottom-left corner
        (556, 447),  # top-left corner
        (720, 447),  # top-right corner
        (1325, 720)  # bottom-right corner
    ], np.float32)



    # Define the corresponding points in the destination (bird's-eye view) image
    pts2 = np.array([
        [0, rows],       # Bottom-left point of the destination image
        [0, 0],          # Top-left point of the destination image
        [cols, 0],       # Top-right point of the destination image
        [cols, rows]     # Bottom-right point of the destination image
    ], np.float32)

    # Compute the perspective transformation matrix using the four corresponding points
    if inverse:
        perspective_transform_matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        perspective_transform_matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Apply the perspective transformation to the input frame
    # The resulting image will be a bird's-eye view of the region of interest
    perspective_transformed_frame = cv2.warpPerspective(frame, perspective_transform_matrix, (cols, rows))

    return perspective_transformed_frame