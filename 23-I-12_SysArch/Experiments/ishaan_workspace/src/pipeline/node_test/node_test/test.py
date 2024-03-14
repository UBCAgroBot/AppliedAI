# import time

# tic = time.perf_counter_ns()
# time.sleep(2)
# toc = time.perf_counter_ns()

# import psutil
# def get_threads_cpu_percent(p, interval=0.1):
#     total_percent = p.cpu_percent(interval)
#     total_time = sum(p.cpu_times())
#     return [('%s %s %s' % (total_percent * ((t.system_time + t.user_time)/total_time), t.id, psutil.Process(t.id).name())) for t in p.threads()]

# # # grab the new total amount of time the process has used the cpu
# # final_total_time = sum(proc.cpu_times())

# # # grab the new system and user times for each thread
# # final_thread_times = {'a': {'system': None, 'user': None}}
# # for thread in proc.threads():
# #     final_thread_times[psutil.Process(thread.id).name()]['system'] = thread.system_time
# #     final_thread_times[psutil.Process(thread.id).name()]['user'] = thread.user_time

# # # calculate how much cpu each thread used by...
# # total_time_thread_a_used_cpu_over_time_interval = ((final_thread_times['a']['system']-initial_thread_times['a']['system']) + (final_thread_times['a']['user']-initial_thread_times['a']['user']))
# # total_time_process_used_cpu_over_interval = final_total_time - initial_total_time

# # percent_of_cpu_usage_utilized_by_thread_a = total_cpu_percent*(total_time_thread_a_used_cpu_over_time_interval/total_time_process_used_cpu_over_interval)

# # check .dockerignore

# try:
#     self.model = torch.jit.load("trt_model.ts").cuda()
# except Exception as e:
#     try:
#         model = torch.load('yolov5s.pt', model_math='fp32').eval().to("cuda") # replace with ONNX
#         self.model = torch_tensorrt.compile(model, inputs=[torch_tensortt([1, 3, 1280, 1280])], enabled_precisions={'torch.half'}, debug=True)
#         self.save = False
#     except Exception as e:
#         self.get_logger().info(f"Error: {e}")
#         raise SystemExit
# finally:
#     self.get_logger().info("Model loaded successfully")
    
#             normalized_image = resized_image / 255.0  # Normalize pixel values to [0, 1]
#         input_image = torch.from_numpy(normalized_image).permute(2, 0, 1).float()  # Convert to torch tensor and rearrange dimensions
#                 output = input_image.unsqueeze(0)  # Add a batch dimension
                
                
#                         img = img.transpose((2, 0, 1)).astype(np.float32)
#         img = np.expand_dims(img, axis=0)

import torch
import torchvision

# Load the PyTorch model
model = torch.load('yolov8x.pt')
model.eval()

# Create a dummy input that matches the input format of the model
# Assuming the model takes a 1x3x224x224 input, but you should adjust this to match your model
dummy_input = torch.randn(1, 3, 640, 640)

# Export the model to an ONNX file
torch.onnx.export(model, dummy_input, "yolov8x.onnx")