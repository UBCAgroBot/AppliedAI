# ROS2 Package For Testing Cpp implementation runtime

This package is used to test the runtime of implementing a ros2 package with cpp. It's meant to be as bare bones as possible. The talker reads/publishes images in the images folder. The listener executable opens the `model.onnx` file and uses it to predict the target labels. 

|  executable | publishes to  | subscribes to  |
| -------- | -------- | -------- |
| talker   | topic   | -   |
| listener   | -  | topic  |

## Running The onnx_cpp node
1. navigate to the `ros2_ws` directory
```bash
rosdep install --from-paths src -y --ignore-src
colcon build --packages-select onnx_cpp
```

2. Open a new Terminal 
```bash
. install/setup.bash
ros2 run onnx_cpp listener
```

3. Open another new terminal
```bash
. install/setup.bash
ros2 run onnx_cpp talker
```




## Common trouble shooting

### Ros2 command not found
run `source /opt/ros/humble/setup.bash` to source the setup files

### colcon build fails because it can't find onnxruntime:
1. Check if onnxruntime is already installed by running `ldconfig -p | grep onnxruntime`
2. If it's not installed, install it:
```bash
# Clone the ONNX Runtime repository
git clone https://github.com/microsoft/onnxruntime.git

# Change directory to the cloned repository
cd onnxruntime

# Build ONNX Runtime
./build.sh --config Release --build_shared_lib --parallel

# Copy the built shared library to /usr/local/lib
sudo cp ./build/Linux/Release/libonnxruntime.so /usr/local/lib

# Update the dynamic linker run-time bindings
sudo ldconfig
```

