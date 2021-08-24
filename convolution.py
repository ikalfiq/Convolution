import cv2
import numpy as np
import time

#cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Output", (720,960))

# Work with region of interest (roi) for greater efficiency
def extract_roi(original_image, input_image, width, height):
    kernel = np.array(
            [[1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]]
            )/16

    # these are variables to keep track of kernel positions and store pixel values before and after calculations
    row, column = 0, 0
    input_roi = []
    region_averages = []

    # output image will be smaller after convolution, so we need to set and account for the correct limits 
    # note that width and height should be smaller to account for array starting from index 0
    kernel_size = kernel.shape[0]
    convolution_widthLimit, convolution_heightLimit = width-3, height-3 
    output_width, output_height = width-2, height-2

    #start = time.time()

    while (True):
        # extract region of interest
        if (row <= convolution_heightLimit and column <= convolution_widthLimit):
            row_segment = input_image[row:row + kernel_size, column:column + kernel_size]
            input_roi.append(row_segment)

            # for loop method increases the time complexity
            #for size in range(kernel_size):
            #    input_roi.append(input_image[row+size][column:column+kernel_size])

            column += 1

            input_roi, kernel = np.array([input_roi]).ravel(), kernel.ravel()
            # matrix multiplication is the fastest way to get convolution sum
            pixel_average = int(input_roi.dot(kernel.T)/ kernel.size)
            region_averages.append(pixel_average)

            # reinitialize the roi list to minimize the number of members 
            input_roi = []
            
        # column overflow, move to next row
        elif (column > convolution_widthLimit):
            column = 0
            row += 1

        # end of image reached
        elif (row > convolution_heightLimit):
            break

    #end = time.time()
    #print("Duration to run while loop:", end-start)
    # display input and output images
    output_image(original_image, input_image, region_averages, output_width, output_height)

def output_image(original_image, input_image, region_averages, width, height):
    # reshape to get the correct dimensions 
    output_image = np.array([region_averages]).reshape(height, width)
    cv2.imwrite("convoluted.jpg", output_image)
    output_image = cv2.imread("convoluted.jpg")
    cv2.imshow("Convoluted", output_image)
    cv2.imshow("Original", original_image)
    cv2.imshow("Gray", input_image)
    print("Done")
    cv2.waitKey(0)

if __name__ == "__main__":

    # OpenCV open image, duplicate so that we don't mess up the original image
    original_input = cv2.imread("test.jpg")
    duplicate_input = original_input.copy()

    height, width = 960, 720

    duplicate_input = cv2.resize(duplicate_input, (width, height))
    original_input = cv2.resize(original_input, (width, height))
    duplicate_input = cv2.cvtColor(duplicate_input, cv2.COLOR_BGR2GRAY)

    extract_roi(original_input, duplicate_input, width, height)
