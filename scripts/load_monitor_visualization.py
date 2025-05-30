#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print("please input file name")
    exit()
  with open(sys.argv[1], 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    x = []
    y = []
    z = []
    cpu = []
    mem = []
    cpu_clock = []
    cpu_temp = []
    for row in csv_reader:
      x.append(float(row[0]))
      y.append(float(row[1]))
      z.append(float(row[2]))
      cpu.append(float(row[3]))
      mem.append(float(row[4]))
      cpu_temp.append(float(row[5]))
      cpu_clock.append(float(row[6]))
  
  fig, axs = plt.subplots(4)
  if (sys.argv[2] == 'time'):
    fig.suptitle("CPU MEM MONITOR")
    axs[0].set_title("CPU LOAD")
    img_cpu_load = axs[0].plot(cpu)
    axs[1].set_title("MEMORY USAGE")
    img_mem_usage = axs[1].plot(np.array(mem))
    axs[2].set_title("CPU TEMPERATURE")
    img_cpu_temp = axs[2].plot(np.array(cpu_temp))
    axs[3].set_title("CPU CLOCK")
    img_cpu_clock = axs[3].plot(np.array(cpu_clock))

  elif (sys.argv[2] == 'pose'):
    fig.suptitle("CPU MEM MONITOR")
    axs[0].set_title("CPU LOAD")
    img_cpu_load = axs[0].scatter(np.array(x), np.array(y), c=np.array(cpu))
    axs[1].set_title("MEMORY USAGE")
    img_mem_usage = axs[1].scatter(np.array(x), np.array(y), c=np.array(mem))
    axs[2].set_title("CPU TEMPERATURE")
    img_cpu_temp = axs[2].scatter(np.array(x), np.array(y), c=np.array(cpu_temp))
    axs[3].set_title("CPU CLOCK")
    img_cpu_clock = axs[3].scatter(np.array(x), np.array(y), c=np.array(cpu_clock))
    plt.colorbar(img_cpu_load, label='Cpu Load', ax=axs[0])
    plt.colorbar(img_mem_usage, label='Mem Usage', ax=axs[1])
    plt.colorbar(img_cpu_temp, label='Cpu Temp', ax=axs[2])
    plt.colorbar(img_cpu_clock, label='Cpu Clock', ax=axs[3])

  plt.show()
  