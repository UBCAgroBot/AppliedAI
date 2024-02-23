import time

tic = time.perf_counter_ns()
print(tic)
time.sleep(2)
toc = time.perf_counter_ns()

print(toc-tic)

# ros2 run node_test jetson_node
# colcon build --packages-select node_test -> --symlink-install
# ensure exec_depend in package.xml matches node's import statements
# The subscriber’s constructor and callback don’t include any timer definition, because it doesn’t need one. Its callback gets called as soon as it receives a message.
# It’s good practice to run rosdep in the root of your workspace (ros2_ws) to check for missing dependencies before building: rosdep install -i --from-path src --rosdistro humble -y
# colcon test to test packages just built
# colcon build --packages-select node_test
# make it delay sending until package is received and processed (buffer processing)
# max cpu usage, initialized variable + comparison, average using metrics later, how to find process IDs
# !!! perf counter is system time (since epoc not process time), rclpy time is process time