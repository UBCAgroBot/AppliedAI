from keras.datasets import fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
image_data = test_images

print(type(image_data[0]))
# ros2 run node_test jetson_node
# colcon build --packages-select node_test -> --symlink-install
# ensure exec_depend in package.xml matches node's import statements
# The subscriber’s constructor and callback don’t include any timer definition, because it doesn’t need one. Its callback gets called as soon as it receives a message.
# It’s good practice to run rosdep in the root of your workspace (ros2_ws) to check for missing dependencies before building: rosdep install -i --from-path src --rosdistro humble -y
# colcon test to test packages just built

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/index.js",
            "stopOnEntry": false,
            "args": [],
            "cwd": "${workspaceFolder}",
            "preLaunchTask": null,
            "runtimeExecutable": null,
            "runtimeArgs": [
                "--nolazy"
            ],
            "env": {
                "NODE_ENV": "development"
            },
            "sourceMaps": false,
            "outFiles": []
        }
    ]
}
