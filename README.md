<div align="center">
  <h1> Advanced Lane Finding</h1>
</div>




https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/b8ffcb73-5062-4929-b224-9aa4725333cf





## Project Goal
Identify the lane lines on the road and create a visual representation of the lane area.

## Steps Involved
- Thresholding: The input frame undergoes thresholding to create a binary image. This technique converts the frame into a black and white image, enhancing the lane markings' visibility.
![Screenshot 2023-08-04 at 05 13 09](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/73f77876-5a52-46a2-bbea-788617e2233c)

- Region of Interest (ROI) Extraction: A specific region of interest is extracted from both the thresholded image and the original frame. This region contains the relevant portion of the image where the lane lines are expected to be present.
![Screenshot 2023-08-04 at 05 13 35](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/5e821e36-bb93-4db4-acf7-46c24c459a2e)

- Perspective Transformation: Perspective transformation is applied to the ROI and the thresholded image. This transformation rectifies the perspective of the image, making it easier to detect parallel lane lines.
![Screenshot 2023-08-04 at 05 13 50](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/b660fa07-0878-4a0e-9391-66c8d24e1394)

- Histogram Calculation: A histogram is computed for the perspective-transformed thresholded image to find the starting points for lane detection. The peaks in the histogram correspond to the positions of the lane lines.
![Screenshot 2023-08-04 at 05 14 16](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/f328ae00-1aeb-4ede-b403-18d0f0e88f55)

- Sliding Window Lane Detection: To detect lane pixels within the identified regions of the image, a sliding window approach is employed. The window slides vertically from the bottom to the top of the image, searching for lane pixels within each window.
![Screenshot 2023-08-04 at 05 14 48](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/8174314d-2d81-4c98-aeda-2f48b94b1941)

- Polynomial Fitting: The detected lane pixels are used to fit second-degree polynomials to both the left and right lane lines. This process allows us to obtain a smooth representation of the lanes.
![Screenshot 2023-08-04 at 05 15 59](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/c2bd29a8-5412-4f8c-beeb-278ce4393443)

- Area Visualization: The area between the detected lane lines is filled, creating a visual representation of the lane area. This area is then transformed back to the original perspective and combined with the original frame to obtain the final output.
![Screenshot 2023-08-04 at 05 16 16](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/716f1116-b94d-4d4f-966f-4038fdbcefb0)
- Debugging and Visualization: The code includes visualization and debugging tools to aid in understanding the lane detection process. These tools can be enabled by setting the 'debug' parameter to 'True' when calling the 'process_frame' function.
![Screenshot 2023-08-04 at 05 16 42](https://github.com/vreabernardo/Advanced-Lane-Finding/assets/45080358/5a135358-7aee-4416-83a6-889a0a500ce4)

## Future Implementations
While the current implementation provides a solid foundation for lane detection, there are several areas for improvement and future enhancements:
- **Robustness to Challenging Conditions:** The current implementation works well under normal road conditions. However, future work could focus on improving lane detection in challenging scenarios, such as low-light conditions, adverse weather, or poorly marked roads.
- **Adaptive Thresholding:** Implementing adaptive thresholding techniques could improve lane detection in varying lighting conditions and handle dynamic environmental changes more effectively.
- **Vehicle Position Estimation:** Extending the project to estimate the vehicle's position relative to the detected lane could enhance its usability in advanced driver assistance systems (ADAS).
- **Traffic Sign Detection:** Integrating traffic sign detection and recognition could enhance the overall system's capabilities, allowing for more advanced driver assistance and safety features.
- **Deep Learning Approaches:** Exploring deep learning techniques, such as convolutional neural networks (CNNs), for lane detection could lead to more accurate and robust results.
- **Multi-Lane Detection:** Extending the project to handle multiple lanes and complex road geometries, such as intersections and highway merges, would be valuable for real-world applications.
