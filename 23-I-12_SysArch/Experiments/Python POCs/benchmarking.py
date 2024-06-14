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
                    print(jetson.cpu['total']['user'])
                    print(jetson.cpu['total']['system'])
                    print(jetson.cpu['total']['idle'])
                    print(jetson.cpu['cpu']['freq'])
                    for name, data in jetson.memory.items():
                        print("------ {name} ------".format(name=name))
                        print(data)
                    for name, data in jetson.gpu.items():
                        print("------ {name} ------".format(name=name))
                        print(data)
                    for key, value in jetson.cpu['total'].items():
                        print("{key}: {value}".format(key=key, value=value))
                    for name, data in jetson.temperature.items():
                        print("------ {name} ------".format(name=name))
                        print(data)
                    for name, data in jetson.power.items():
                        print("------ {name} ------".format(name=name))
                        print(data)
                    
                count += 1
                time.sleep(1)
    
    print("Logging finished")