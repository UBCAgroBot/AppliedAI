cmake_minimum_required(VERSION 3.5)
project(cpp_test)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(sensor_msgs REQUIRED)

include_directories(
  ${rclcpp_INCLUDE_DIRS}
)

add_executable(cpp_pub src/cpp_pub.cpp)
add_executable(cpp_sub src/cpp_sub.cpp)

install(TARGETS 
  cpp_pub
  cpp_sub
  DESTINATION lib/${PROJECT_NAME})

ament_package()
