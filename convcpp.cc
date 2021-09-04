// To compile with opencv, need to include link to libraries: `pkg-config --cflags --libs opencv4`
// include relevant OpenCV libraries
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp> // relevant for image processing such as resize
#include <opencv2/highgui.hpp>

#include <iostream>
#include <vector>

int calculate_convolution (cv::Mat input_roi, cv::Mat kernel) {
	int dot_product = input_roi.dot(kernel);
	//std::cout << dot_product << std::endl;

	cv::Mat sum_matrix = cv::Mat::ones(3,3, CV_8UC1);
	int kernel_sum = kernel.dot(sum_matrix);

	return dot_product/kernel_sum;
}

void output_image(cv::Mat original_image, cv::Mat input_image, std::vector<double> region_averages, int width, int height) {
	// can only convert from vector to matrix if vector is of type: double
	cv::Mat1d averages(height-2, width-2, region_averages.data(), CV_8UC1);
	/* 
	// check if dimensions match
	std::vector<double>::iterator iterator;
	
	iterator= region_averages.begin();
	for (iterator=region_averages.begin(); iterator < region_averages.begin()+718; iterator++) {
		std::cout << *iterator << ", ";
	}
	std::cout << std::endl << "averages: "<< std::endl;

	std::cout << averages.row(0) << std::endl;
	*/
	std::cout << averages.type() << std::endl;
	std::cout << input_image.type() << std::endl;

	cv::imwrite("C++_output.jpg", averages);
	cv::Mat read_file = cv::imread("C++_output.jpg");
	cv::imshow("After convolution", read_file);
	cv::imshow("Before convolution", input_image);
	cv::waitKey(0);

}

void extract_roi(cv::Mat original_image, cv::Mat input_image, int width, int height) {
	// declaring n x n matrix in C++ using OpenCV matrix format 
	cv::Mat kernel = cv::Mat(3, 3, CV_8UC1);
	//std::cout << kernel << std::endl;
	
	kernel.rowRange(0,3) = 1;
	kernel.colRange(0,3) = 1;

	/*
	// better way to assign the values?
	kernel.row(0).col(0) = 1; kernel.row(0).col(1) = 2; kernel.row(0).col(2) = 1; 
	kernel.row(1).col(0) = 2; kernel.row(1).col(1) = 4; kernel.row(1).col(2) = 2;
	kernel.row(2).col(0) = 1; kernel.row(2).col(1) = 2; kernel.row(2).col(2) = 1;
	*/

	// variables to keep track of position of kernel
	int row = 0, column = 0;
	std::vector<double> region_averages;

	cv::Size s = kernel.size();
	int kernel_size = s.width;
	std::cout << kernel_size << std::endl;
	int conv_width = width-3, conv_height = height-3;
	int output_width = width-2, output_height = height-2;

	cv::Mat input_roi;
	// extracting the roi
	while (true) {
		if (row <= conv_height && column <= conv_width) {
			input_roi = input_image(cv::Range(row, row+kernel_size), cv::Range(column, column+kernel_size));
			//std::cout << input_roi << std::endl;
			// do the dot product
			region_averages.push_back(calculate_convolution(input_roi, kernel));
			column += 1;
		} 

		else if (column > conv_width) {
			column = 0;
			row += 1;

		}

		else if (row > conv_height) {
			break;
		}
	}

	output_image(original_image, input_image, region_averages, width, height);

}

int main() {
	cv::Mat raw_input = cv::imread("test.jpg", CV_8UC1);	
	cv::Mat duplicated_input = raw_input.clone(); 
	// convert to grayscale for quicker computation
	//cv::cvtColor(duplicated_input, duplicated_input, cv::COLOR_BGR2GRAY);
	
	int height = 960, width = 720;

	// resize to fit into screen
	cv::Mat resized_image;
	cv::resize(duplicated_input, resized_image, cv::Size(width, height));
	cv::resize(raw_input, raw_input, cv::Size(width, height));

	extract_roi(raw_input, resized_image, width, height);

	return 0;
}
