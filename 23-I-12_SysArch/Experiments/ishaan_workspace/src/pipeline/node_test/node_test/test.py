from keras.datasets import fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
image_data = test_images

print(type(image_data[0]))
# ros2 run node_test jetson_node
# colcon build --packages-select node_test
# source install/setup.bash

# add embedded testing methods
# on surface: echo "source install/setup.bash" >> ~/.bashrc
# pipeline for metric evaluation
# logging metrics somewhere
# use open CV pipleine w/ bridge
# simple yolo bounding + launch window
# node architecture testing via launch file
# record highest value in header
# !!! rgbd camera considerations...
# make zed camrea feed publisher + start tet yolo application + viewer window -> how test acc?
# 3rd topic research after finished openCV + dashboard + more ROS tutorials

# max cpu usage, initialized variable + comparison, average using metrics later, how to find process IDs
# colcon test to test packages just built
# ROS tutorials go hard after finishing zed camera interfacing
