import time

tic = time.perf_counter_ns()
time.sleep(2)
toc = time.perf_counter_ns()

import psutil
def get_threads_cpu_percent(p, interval=0.1):
    total_percent = p.cpu_percent(interval)
    total_time = sum(p.cpu_times())
    return [('%s %s %s' % (total_percent * ((t.system_time + t.user_time)/total_time), t.id, psutil.Process(t.id).name())) for t in p.threads()]

# Get 1 available GPU, ordered by GPU load ascending
# print('First available weighted by GPU load ascending: '),
# print(GPU.getAvailable(order='load', limit=1))

gpu = GPUtil.getGPUs()[0] # firstGPU = GPU.getFirstAvailable()

# Get 1 available GPU, ordered by ID in descending order
# print('Last available: '),
# print(GPU.getAvailable(order='last', limit=1))  

# better put in separate process
# from tqdm import tqdm
# from time import sleep
# import psutil

# with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
#     while True:
#         rambar.n=psutil.virtual_memory().percent
#         cpubar.n=psutil.cpu_percent()
#         rambar.refresh()
#         cpubar.refresh()
#         sleep(0.5)

# # if fancy CPU measure no work: 

# function here

# latency might require adding milliseconds + nanoseconds together?

# # grab the new total amount of time the process has used the cpu
# final_total_time = sum(proc.cpu_times())

# # grab the new system and user times for each thread
# final_thread_times = {'a': {'system': None, 'user': None}}
# for thread in proc.threads():
#     final_thread_times[psutil.Process(thread.id).name()]['system'] = thread.system_time
#     final_thread_times[psutil.Process(thread.id).name()]['user'] = thread.user_time

# # calculate how much cpu each thread used by...
# total_time_thread_a_used_cpu_over_time_interval = ((final_thread_times['a']['system']-initial_thread_times['a']['system']) + (final_thread_times['a']['user']-initial_thread_times['a']['user']))
# total_time_process_used_cpu_over_interval = final_total_time - initial_total_time

# percent_of_cpu_usage_utilized_by_thread_a = total_cpu_percent*(total_time_thread_a_used_cpu_over_time_interval/total_time_process_used_cpu_over_interval)