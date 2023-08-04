<div align="center">
  <h1> Advanced Lane Finding</h1>
</div>



https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/eb389fd4-be75-493c-b9a9-373d83a700f6



## Project Overview
The Advanced Lane Finding project focuses on detecting and tracking lane lines in images or video frames using computer vision techniques. The primary goal is to identify the lane lines on the road and create a visual representation of the lane area.

## Steps Involved
- Thresholding: The input frame undergoes thresholding to create a binary image. This technique converts the frame into a black and white image, enhancing the lane markings' visibility.
q![Screenshot 2023-08-04 at 05 01 32](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/180e47de-592b-4675-ba4f-9601091350ac)

- Region of Interest (ROI) Extraction: A specific region of interest is extracted from both the thresholded image and the original frame. This region contains the relevant portion of the image where the lane lines are expected to be present.
![Screenshot 2023-08-04 at 05 02 30](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/61c0d1c4-a809-4af2-9d01-1fa5ff4ba60b)

- Perspective Transformation: Perspective transformation is applied to the ROI and the thresholded image. This transformation rectifies the perspective of the image, making it easier to detect parallel lane lines.
![Screenshot 2023-08-04 at 05 03 04](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/4f5ea6da-9d82-4b9c-aaa4-f9bc5a5dea9a)

- Histogram Calculation: A histogram is computed for the perspective-transformed thresholded image to find the starting points for lane detection. The peaks in the histogram correspond to the positions of the lane lines.
1![Screenshot 2023-08-04 at 05 03 23](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/eb89efee-9a40-484a-b8a5-ff3397ee2ca3)

- Sliding Window Lane Detection: To detect lane pixels within the identified regions of the image, a sliding window approach is employed. The window slides vertically from the bottom to the top of the image, searching for lane pixels within each window.
![Screenshot 2023-08-04 at 05 04 04](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/bac33fdf-d661-4ff6-a4c6-5b23bbbb55b0)

- Polynomial Fitting: The detected lane pixels are used to fit second-degree polynomials to both the left and right lane lines. This process allows us to obtain a smooth representation of the lanes.
![Screenshot 2023-08-04 at 05 04 42](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/7409c21e-f72f-4c24-94ba-4a836748325f)

- Area Visualization: The area between the detected lane lines is filled, creating a visual representation of the lane area. This area is then transformed back to the original perspective and combined with the original frame to obtain the final output.
![Screenshot 2023-08-04 at 05 05 07](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/63de2f76-00e1-407d-804c-09ca37c37d43)

- Debugging and Visualization: The code includes visualization and debugging tools to aid in understanding the lane detection process. These tools can be enabled by setting the 'debug' parameter to 'True' when calling the 'process_frame' function.
![Screenshot 2023-08-04 at 05 09 50](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/f3606ade-c005-45eb-ad79-d7f1e7b3b30d)
