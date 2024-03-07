#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <thread>
#include <curses.h>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "std_msgs/msg/header.hpp"
#include "sl/Camera.hpp"

class MinimalPublisher : public rclcpp::Node
{
  public:
    MinimalPublisher()
    : Node("minimal_publisher")
    {
      publisher_ = this->create_publisher<sensor_msgs::msg::Image>("topic", 10);

      // Initialize ZED camera
      sl::InitParameters init_params;
      init_params.camera_resolution = sl::RESOLUTION_HD720;
      init_params.camera_fps = 60;
      zed_.open(init_params);

      // Start a separate thread to listen for keyboard input
      std::thread keyboard_listener([this]() {
        initscr();
        cbreak();
        noecho();
        timeout(0);

        while (rclcpp::ok()) {
          int c = getch();
          if (c == 'q') {
            rclcpp::shutdown();
          }
        }

        endwin();
      });

      // Capture and publish images
      while (rclcpp::ok()) {
        capture_and_publish_image();
      }

      // Join the keyboard listener thread
      keyboard_listener.join();
    }

  private:
    void capture_and_publish_image()
    {
      sl::Mat image_zed;
      if (zed_.grab() == sl::SUCCESS) {
        zed_.retrieveImage(image_zed, sl::VIEW_LEFT);
        auto img_msg = slMat2cvMat(image_zed);

        // Create a header for the image
        std_msgs::msg::Header header;
        header.stamp = this->now();

        // Set the header in the image message
        img_msg->header = header;

        RCLCPP_INFO(this->get_logger(), "Publishing image");
        publisher_->publish(*img_msg);
      }
    }

    sensor_msgs::msg::Image::SharedPtr slMat2cvMat(sl::Mat& input)
    {
      // Convert the sl::Mat to cv::Mat
      cv::Mat mat(input.getHeight(), input.getWidth(), CV_8UC4, input.getPtr<sl::uchar1>(sl::MEM_CPU));
      auto img_msg = cv_bridge::CvImage(std_msgs::msg::Header(), "bgra8", mat).toImageMsg();
      return img_msg;
    }

    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
    sl::Camera zed_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  std::make_shared<MinimalPublisher>();
  return 0;
}