#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>

namespace py = pybind11;

std::vector<std::vector<int>> object_filter(py::array_t<uint8_t> input_image, py::tuple bounding_box) {
    // numpy array to a cv::Mat
    py::buffer_info buf = input_image.request();
    cv::Mat image(buf.shape[0], buf.shape[1], CV_8UC3, (unsigned char*)buf.ptr);

    // bounding box coordinates
    int x1 = bounding_box[0].cast<int>();
    int y1 = bounding_box[1].cast<int>();
    int x2 = bounding_box[2].cast<int>();
    int y2 = bounding_box[3].cast<int>();

    // Region of Interest
    cv::Mat roi = image(cv::Rect(x1, y1, x2 - x1, y2 - y1));

    // color segmentation mask
    cv::Mat hsv;
    cv::cvtColor(image, hsv, cv::COLOR_RGB2HSV);
    cv::Mat mask;
    cv::inRange(hsv, cv::Scalar(78, 158, 124), cv::Scalar(60, 255, 255), mask);
    cv::Mat result;
    cv::bitwise_and(image, image, result, mask);

    // Find bounding boxes
    cv::Rect bbox = cv::boundingRect(mask);

    std::vector<std::vector<int>> detections;
    if (bbox.area() > 0) {
        detections.push_back({bbox.x, bbox.y, bbox.width, bbox.height});
    }

    // Additional contour detection
    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(mask, contours, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);
    for (auto& cnt : contours) {
        if (cv::contourArea(cnt) > 100) {
            cv::Rect cnt_bbox = cv::boundingRect(cnt);
            detections.push_back({cnt_bbox.x, cnt_bbox.y, cnt_bbox.width, cnt_bbox.height});
        }
    }

    return detections;
}

PYBIND11_MODULE(object_filter, m) {
    m.def("object_filter", &object_filter, "A function that filters objects in an image",
          py::arg("input_image"), py::arg("bounding_box"));
}