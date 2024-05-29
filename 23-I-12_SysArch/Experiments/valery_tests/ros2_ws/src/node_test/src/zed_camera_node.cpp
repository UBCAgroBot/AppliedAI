#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include <sl/Camera.hpp>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.hpp>
#include "sensor_msgs/msg/image.hpp"

using namespace std::chrono_literals;
using namespace cv;
using namespace std::chrono_literals;
using namespace std::placeholders;
using namespace sl;

//GPU mat, if easier, can use a while loop for if q key pressed and then break zed camera and raise exception
//ask copilot to make same version of this for regular old webcam
//alter for dynamic runtime args later

class ZedPublisher : public rclcpp::Node
{
public:
  ZedPublisher() : Node("zed_publisher"), zed(), count_(0)
  {
    // Initialize the ZED camera
    Camera zed; // Create a ZED camera object
    InitParameters init_params; // Set initial parameters
    init_params.sdk_verbose = 0; // Disable verbose mode
    init_params.camera_resolution = RESOLUTION::HD1080; // Use HD1080 video mode
    init_params.camera_fps = 30; // Set fps at 30

    // Open Zed camera
    ERROR_CODE err = zed.open(init_params);
    if (err != ERROR_CODE::SUCCESS)
      RCLCPP_ERROR(this->get_logger(), "Failed to open the ZED camera");
      rclcpp::shutdown();
      return;

    // Initialize the ZED camera
    if (zed.open() != ERROR_CODE::SUCCESS) {
      RCLCPP_ERROR(this->get_logger(), "Failed to open the ZED camera");
      rclcpp::shutdown();
      return;
    }

    // Create a publisher
    camera_image_ = this->create_publisher<sensor_msgs::msg::Image>("zed_image", 10);

    // Start a new thread that captures and publishes frames
    std::thread(&ZedPublisher::capture_and_publish, this).detach();
  }

private: 
  void capture_and_publish()
  {
    // Create a sl::Mat object (4 channels of type unsigned char) to store the image.
    sl::Mat raw_zed(zed.getResolution(), MAT_TYPE::U8_C4);
    // Create an OpenCV Mat that shares sl::Mat data
    cv::Mat image_ocv = slMat2cvMat(raw_zed);
    while (rclcpp::ok()) {
      if (zed.grab() == ERROR_CODE::SUCCESS) {
        // Retrieve the left image in sl::Mat
        // The cv::Mat is automatically updated
        zed.retrieveImage(image_zed, VIEW::LEFT);

        // Convert BGRA to BGR using OpenCV
        cv::Mat image_bgr;
        cv::cvtColor(image_ocv, image_bgr, cv::COLOR_BGRA2BGR);

        auto current_time = std::chrono::system_clock::now();
        auto time_in_ms = std::chrono::duration_cast<std::chrono::milliseconds>(current_time.time_since_epoch()).count()

        std_msgs::msg::Header header = std_msgs::msg::Header(); // empty header
        header.frame_id = "image_" + std::to_string(count_++ % 10); // time

        cv_bridge::CvImage img_bridge = cv_bridge::CvImage(header, sensor_msgs::image_encodings::BGR8, image_bgr);

        sensor_msgs::msg::Image out_image; // >> message to be sent
        img_bridge.toImageMsg(out_image); // from cv_bridge to sensor_msgs::Image

        auto message = std_msgs::msg::String();
        RCLCPP_INFO(this->get_logger(), "Published image frame %s at time %lld", header.frame_id.c_str(), time_in_ms);
        camera_image_->publish(out_image);
      }
    }
  }
};

int main(int argc, char * argv[])
{
  // Force flush of the stdout buffer.
  setvbuf(stdout, NULL, _IONBF, BUFSIZ);
  
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ZedPublisher>());
  rclcpp::shutdown();
  zed.close();
  return 0;
}