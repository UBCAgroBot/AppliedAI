from keras.datasets import fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
image_data = test_images

print(type(image_data[0]))
# ros2 run note_test jetson_node
# colcon build --packages-select node_test
# source install/setup.bash