from jtop import jtop
import csv
import argparse
import os
import time

# arguments: --duration 1 --file jtop.csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple jtop logger')
    parser.add_argument('--duration', action="store", dest="duration", default=1) # 1 minute
    parser.add_argument('--file', action="store", dest="file", default="jtop.csv")
    parser.add_argument('--verbose', action="store_true", dest="verbose", default=True)
    
    args = parser.parse_args()
    
    with jtop() as jetson:
        with open(args.file, 'w') as csvfile:
            count = 0
            stats = jetson.stats
            # Initialize cws writer
            writer = csv.DictWriter(csvfile, fieldnames=stats.keys())
            # Write header
            writer.writeheader()
            # Write first row
            writer.writerow(stats)
            # Start loop
            os.system("clear") # start ros2 launch
            while jetson.ok() and count < args.duration * 60:
                stats = jetson.stats
                # Write row
                writer.writerow(stats)
                print("Log at {time}".format(time=stats['time']))
                if args.verbose:
                    # user_cpu = jetson.cpu['total']['user']
                    # system_cpu = jetson.cpu['total']['system']
                    # idle_cpu = jetson.cpu['total']['idle']
                    # cpu = 1 - (idle_cpu/(user_cpu + system_cpu + idle_cpu))
                    cpu_usage = 1 - jetson.cpu['total']['idle']
                    memory_usage = (jetson.memory['RAM']['used']/jetson.memory['total'])*100
                    gpu_usage = (jetson.gpu['ga10b']['status']['load'])
                    gpu_frequency = (jetson.gpu['ga10b']['freq']['cur'])
                    cpu_temp = (jetson.temperature['CPU']['temp'])
                    gpu_temp = (jetson.temperature['GPU']['temp'])
                    system_voltage = (jetson.power['tot']['volt'])
                    system_current = (jetson.power['tot']['curr'])
                    system_power = (jetson.power['tot']['power'])
                    
                    print(f"CPU Usage: {cpu_usage}%")
                    print(f"Memory Usage: {memory_usage}%")
                    print(f"GPU Usage: {gpu_usage}%")
                    print(f"GPU Frequency: {gpu_frequency} MHz")
                    print(f"CPU Temperature: {cpu_temp}°C")
                    print(f"GPU Temperature: {gpu_temp}°C")
                    print(f"System Voltage: {system_voltage} V")
                    print(f"System Current: {system_current} A")
                    print(f"System Power: {system_power} W")
                    
                    # for name, data in jetson.memory.items():
                    #     print("------ {name} ------".format(name=name))
                    #     print(data)
                    # for name, data in jetson.gpu.items():
                    #     print("------ {name} ------".format(name=name))
                    #     print(data)
                    # for key, value in jetson.cpu['total'].items():
                    #     print("{key}: {value}".format(key=key, value=value))
                    # for name, data in jetson.temperature.items():
                    #     print("------ {name} ------".format(name=name))
                    #     print(data)
                    # for name, data in jetson.power.items():
                    #     print("------ {name} ------".format(name=name))
                    #     print(data)
                    
                count += 1
                time.sleep(1)
    
    print("Logging finished")