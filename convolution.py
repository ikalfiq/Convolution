import cv2
import numpy as np

#cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Output", (720,960))

# Work with region of interest (roi) for greater efficiency
def extract_roi(img, width, height):
    # Define the kernel and image region of interest
    kernel = np.array(
            [[1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]]
            )/16

    row, column = 0, 0
    img_roi = []
    region_averages = []

    kernel_threshold, kernel_size = kernel.shape[0] - 1, kernel.shape[0]

    while (True):
        # Get the region of interest
        if (row+kernel_threshold <= height - 1 and column+kernel_threshold <=  width-1):
            for size in range(kernel_size):
                img_roi.append(img[row+size][column:column+kernel_size])

            # Track the row and column for convenience
            #print("Row:", row)
            #print("Column:", column)
            column += 1
            region_averages.append(calculate(img_roi, kernel))
            # Reinitialize the roi list to minimize the number of members 
            img_roi = []
            #break # This is to stop at the first iteration
            
        # Column overflow
        elif (column+kernel_threshold > width-1):
            column = 0
            row += 1

        # Reach end of image
        elif (row+kernel_threshold > height - 1):
            break

    # print(len(averages)) # Number of members correspond to number of pixels for convoled image

    # Proceed to display the output image
    output_image(img, region_averages, width-kernel_threshold, height-kernel_threshold)

def calculate(img_roi, kernel):
    img_roi, kernel = np.array(img_roi).ravel(), kernel.ravel()
    #print(img_roi, kernel)

    # Matrix multiplication is the fastest way to get convolution sum
    average_value = int(img_roi.dot(kernel.T)/ kernel.size)
    #print(average_value)
    return average_value

def output_image(default_image, region_averages, width, height):
    # Reorganize the list such that you end up with a 718x958 image
    region_averages = np.array([region_averages]).reshape(height, width)
    cv2.imwrite("Convoluted.jpg", region_averages)
    convoluted_pic = cv2.imread("Convoluted.jpg")
    cv2.imshow("Convoluted", convoluted_pic)
    cv2.imshow("Default", default_image)
    #cv2.imshow("Convoluted", region_averages)
    print("Done")
    cv2.waitKey(0)

if __name__ == "__main__":

    # OpenCV open image, duplicate so that we don't mess up the original image
    input_img = cv2.imread("test.jpg")
    duplicate_input = img.copy()

    height, width = 960, 720
    #height, width = 12, 12 

    duplicate_input = cv2.resize(duplicate, (width, height))
    duplicate_input = cv2.cvtColor(duplicate, cv2.COLOR_BGR2GRAY)

    extract_roi(duplicate_input, width, height)

    cv2.waitKey(0)
    
