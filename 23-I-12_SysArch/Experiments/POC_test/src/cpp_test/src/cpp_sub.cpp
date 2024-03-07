#include <functional>
#include <memory>
#include <chrono>
#include <ctime>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"

#include <opencv2/opencv.hpp> 
#include <cv_bridge/cv_bridge.h>

using std::placeholders::_1;
using namespace cv;

class MinimalSubscriber : public rclcpp::Node
{
  public:
    MinimalSubscriber()
    : Node("minimal_subscriber")
    {
      subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
      "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
    // Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "ModelRunner");
    }

  private:
    void topic_callback(const sensor_msgs::msg::Image::Sharedptr & msg) const
    {
      auto now = this->now();
      auto latency = now - msg->header.stamp;
      RCLCPP_INFO(this->get_logger(), "Latency: '%ld'", latency.nanoseconds());
    }
      cv_bridge::CvImagePtr cv_ptr;
      try
      {
        cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
      }
      catch (cv_bridge::Exception& e)
      {
        RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
        return;

      // Display the image using OpenCV
      cv::namedWindow("Image Window", cv::WINDOW_NORMAL);
      cv::imshow("Image Window", cv_ptr->image);
      cv::waitKey(3);
      }
    
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;
};



int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  return 0;
}