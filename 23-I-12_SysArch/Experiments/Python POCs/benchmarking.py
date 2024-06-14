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
                    # for key, value in stats.items():
                    #     print("{key}: {value}".format(key=key, value=value))
                    print(jetson.cpu)
                    print(jetson.gpu)
                    print(jetson.memory)
                    print(jetson.temperature)
                    print(jetson.power)
                count += 1
                time.sleep(1)
    
    print("Logging finished")
            
                # for idx, cpu in enumerate(jetson.cpu['cpu']):
                #     print("------ CPU{idx} ------".format(idx=idx))
                #     for key, value in cpu.items():
                #         print("{key}: {value}".format(key=key, value=value))
                # total = jetson.cpu['total']
                # print("------ TOTAL ------")
                # for key, value in total.items():
                #     print("{key}: {value}".format(key=key, value=value))
                
                # for name, data in jetson.memory.items():
                #     print("------ {name} ------".format(name=name))
                #     print(data)
                # for name, data in jetson.gpu.items():
                #     print("------ {name} ------".format(name=name))
                #     print(data)