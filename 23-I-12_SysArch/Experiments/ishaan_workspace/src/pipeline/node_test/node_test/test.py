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
# launch file
# logging metrics somewhere
# use open CV pipleine w/ bridge
# simple yolo bounding + launch window
# peek next architecture type
# node architecture testing via launch file
# record highest value in header
