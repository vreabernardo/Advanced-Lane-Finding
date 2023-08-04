import cv2
import numpy as np
import thresholding as thr
import debugTools as dbt
import perspective_transform as pt

def process_frame(frame, debug=False):
    # Threshold the frame to create a binary image
    ColorThresholdImage = thr.ThresholdBinaryImage(frame)

    # Extract the region of interest (ROI) from the thresholded image
    edges_ROI = cv2.bitwise_and(ColorThresholdImage, ColorThresholdImage, mask=thr.create_mask(ColorThresholdImage))
    frame_ROI = cv2.bitwise_and(frame, frame, mask=thr.create_mask(frame))

    # Apply perspective transformation to the ROI and the thresholded image
    edges_perspective_transform = pt.create_perspective_transform(edges_ROI)
    frame_perspective_transform = pt.create_perspective_transform(frame_ROI)

    # Stack the perspective-transformed edge image with two zero channels to create a 3-channel image
    edges_perspective_transform_color = cv2.merge((edges_perspective_transform, np.zeros_like(edges_perspective_transform), np.zeros_like(edges_perspective_transform)))

    # Calculate histogram to find starting points for lane detection
    histogram = np.sum(edges_perspective_transform[int(edges_perspective_transform.shape[0] / 2):, :], axis=0)
    midpoint = histogram.shape[0] // 2
    maxLeft = np.argmax(np.split(histogram, 2)[0])
    maxRight = np.argmax(np.split(histogram, 2)[1]) + midpoint

    # Perform sliding window lane detection and fit polynomial to the lane lines
    left_fit, right_fit = sliding_window_lane_detection(
        edges_perspective_transform_color,
        frame_perspective_transform,
        maxLeft, maxRight)

    # Get the area between the lane lines and transform it back to the original perspective
    area = plotLines(left_fit, right_fit, frame_perspective_transform)
    area_inROI = pt.create_perspective_transform(area, True)

    if debug:
        dbt.plot_histogram_with_legend(histogram, maxLeft, maxRight)

    # Invert the mask to restore the rest of the frame except the ROI
    mask_inverted = cv2.bitwise_not(thr.create_mask(frame_ROI))

    # Combine the restored frame with the area_inROI to get the final output
    restored_frame = cv2.bitwise_and(frame, frame, mask=mask_inverted)
    restored_frame = cv2.bitwise_or(restored_frame, area_inROI)

    return restored_frame

def plotLines(left_fit, right_fit, frame):
    plot = np.linspace(0, frame.shape[0] - 1, frame.shape[0])
    left_fitx = left_fit[0] * plot ** 2 + left_fit[1] * plot + left_fit[2]
    right_fitx = right_fit[0] * plot ** 2 + right_fit[1] * plot + right_fit[2]

    for y, left_x, right_x in zip(plot.astype(int), left_fitx.astype(int), right_fitx.astype(int)):
        cv2.circle(frame, (left_x, y), 2, (0, 255, 0), 15)
        cv2.circle(frame, (right_x, y), 2, (0, 255, 0), 15)


    # Filling the area between the lane lines
    lane_area = np.zeros_like(frame)
    pts_left = np.array([np.transpose(np.vstack([left_fitx, plot]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, plot])))])
    pts = np.hstack((pts_left, pts_right))
    cv2.fillPoly(lane_area, np.int_([pts]), (0, 255, 0))

    lane_area_on_transformed = cv2.addWeighted(frame, 1, lane_area, 0.3, 0)
    return lane_area_on_transformed



def sliding_window_lane_detection(edgeFrame, normalFrame, maxLeft, maxRight):
    # Number of sliding windows to divide the image vertically
    n_windows = 9

    # Calculate the height of each window
    window_height = int(edgeFrame.shape[0] / n_windows)

    # Get the indices of nonzero pixels in the grayscale image (representing edges)
    nonzero_pixels = edgeFrame.nonzero()
    nonzero_y = np.array(nonzero_pixels[0])
    nonzero_x = np.array(nonzero_pixels[1])

    # Initialize current x-coordinates for the left and right lane lines
    leftx_current = maxLeft
    rightx_current = maxRight

    # Define the margin around the current lane lines within which to search for lane pixels (window x)
    margin = 100

    # Minimum number of pixels required in a window to recenter the sliding window
    min_pixels = 50

    # Lists to store the indices of left and right lane pixels for each window
    left_lane_indices = []
    right_lane_indices = []

    # Iterate through each window from the bottom of the image to the top
    for window in range(n_windows):
        # Calculate the y-range of the current window
        win_y_low = edgeFrame.shape[0] - (window + 1) * window_height
        win_y_high = edgeFrame.shape[0] - window * window_height

        # Calculate the x-ranges of the left and right windows
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin

        # Draw green rectangles to visualize the sliding windows on the original and edge images
        cv2.rectangle(edgeFrame, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high), (0, 0, 255), 5)
        cv2.rectangle(edgeFrame, (win_xright_low, win_y_low), (win_xright_high, win_y_high), (0, 0, 255), 5)

        cv2.rectangle(normalFrame, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high), (0, 0, 255), 5)
        cv2.rectangle(normalFrame, (win_xright_low, win_y_low), (win_xright_high, win_y_high), (0, 0, 255), 5)

        # Identify nonzero edge pixels within the left and right windows
        good_left_indices = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) &
                             (nonzero_x >= win_xleft_low) & (nonzero_x < win_xleft_high)).nonzero()[0]
        good_right_indices = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) &
                              (nonzero_x >= win_xright_low) & (nonzero_x < win_xright_high)).nonzero()[0]

        # Append the indices to the respective lists
        left_lane_indices.append(good_left_indices)
        right_lane_indices.append(good_right_indices)

        # Update the current x-coordinates if enough pixels are found in the window
        if len(good_left_indices) > min_pixels:
            leftx_current = int(np.mean(nonzero_x[good_left_indices]))
        if len(good_right_indices) > min_pixels:
            rightx_current = int(np.mean(nonzero_x[good_right_indices]))

    # Concatenate the lists of indices into arrays
    left_lane_indices = np.concatenate(left_lane_indices)
    right_lane_indices = np.concatenate(right_lane_indices)

    # Get the x and y coordinates of the identified pixels for the left and right lanes
    leftx = nonzero_x[left_lane_indices]
    lefty = nonzero_y[left_lane_indices]
    rightx = nonzero_x[right_lane_indices]
    righty = nonzero_y[right_lane_indices]

    # Fit second-degree polynomials to the identified points for the left and right lanes
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    return left_fit, right_fit


if __name__ == "__main__":
    video_file = 'project_video.mp4'
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print("Error opening video file")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            processed_frame = process_frame(frame, debug=False)
            cv2.imshow('video', processed_frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()