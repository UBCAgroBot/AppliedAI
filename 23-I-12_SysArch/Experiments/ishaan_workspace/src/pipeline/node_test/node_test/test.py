import time

tic = time.perf_counter_ns()
time.sleep(2)
toc = time.perf_counter_ns()

class Trendy():
    def __init__(self):
        self.fps, self.mem, self.time, self.cpu = 0, 0, 0, 0
        self.metrics = [self.fps, self.mem, self.time, self.cpu]
    
    def try_again(self):
        for metric in self.metrics:
            self.metric = 1
    
    def leol(self):
        for metric in self.metrics:
            print(self.metric)

if __name__ == "__main__":
    self = Trendy()
    self.try_again()
    self.leol()

# import psutil, sys, time, os

# def clear():
#     if os.name == "nt":
#         _ = os.system("cls")
#     else:
#         _ = os.system("clear")

# def get_threads_cpu_percent(p, interval=0.1):
#    total_percent = p.cpu_percent(interval)
#    total_time = sum(p.cpu_times())
#    return [('%s %s %s' % (total_percent * ((t.system_time + t.user_time)/total_time), t.id, psutil.Process(t.id).name())) for t in p.threads()]

# # better put in separate process
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
# pre_cpu = psutil.Process(pid).cpu_percent(interval=None)
# # function here
# post_cpu = psutil.Process(pid).cpu_percent(interval=None)

# run cpu_percent() periodically in a separate thread. 
# If your cpu_percent function returns the total CPU usage of all processes, subtracting the original usage before running from the usage after running (what you're doing) should work.

# latency might require adding milliseconds + nanoseconds together?