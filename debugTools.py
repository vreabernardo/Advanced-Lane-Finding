import cv2
import matplotlib.pyplot as plt

def debugKernel(frame):

    kernelSizes = {
        'small': [(3, 3), (5, 5)],
        'medium': [(7, 7), (9, 9)],
        'large': [(11, 11), (15, 15)]
    }

    edgesList = []
    for key, sizes in kernelSizes.items():
        for size in sizes:
            edges = frameToEdges(frame, 50, 150, kernelSize=size)
            edgesList.append(edges)

    return edgesList

def frameToEdges(frame,th1, th2,kernelSize=(5, 5)):
    """threshold1 (50) for weak edges and threshold2 (150) for strong edges."""

    blur = cv2.GaussianBlur(frame, kernelSize, 0)
    edges = cv2.Canny(blur, threshold1=th1, threshold2=th2)

    return edges

def plot_histogram_with_legend(histogram, leftx_base, rightx_base):

    """
    Plot the histogram with base positions of the lanes.

    Parameters:
        histogram (numpy.ndarray): Lane histogram.
        leftx_base (int): Base position of the left lane.
        rightx_base (int): Base position of the right lane.

    Returns:
        None
    """

    plt.plot(histogram, label='Histogram')
    plt.axvline(x=leftx_base, color='r', linestyle='--', label='Left Base')
    plt.axvline(x=rightx_base, color='g', linestyle='--', label='Right Base')
    plt.xlabel('Pixel Columns')
    plt.ylabel('Counts')
    plt.title('Histogram of Birdseye View')
    plt.legend()

    plt.show(block=False)
    plt.pause(0.0001)
    plt.clf()
