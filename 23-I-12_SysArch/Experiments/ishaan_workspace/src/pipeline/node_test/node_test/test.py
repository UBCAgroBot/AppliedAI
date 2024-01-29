from keras.datasets import fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
image_data = test_images

print(type(image_data[0]))
# ros2 run node_test jetson_node
# colcon build --packages-select node_test -> --symlink-install

# metrics logging file
# use open CV pipleine w/ bridge
# simple yolo bounding + launch window
# node architecture testing via launch file
# record highest value in header
# !!! rgbd camera considerations...
# make zed camrea feed publisher + start tet yolo application + viewer window -> how test acc?

# ensure exec_depend in package.xml matches node's import statements
# The subscriber’s constructor and callback don’t include any timer definition, because it doesn’t need one. Its callback gets called as soon as it receives a message.
# It’s good practice to run rosdep in the root of your workspace (ros2_ws) to check for missing dependencies before building: rosdep install -i --from-path src --rosdistro humble -y
# colcon test to test packages just built