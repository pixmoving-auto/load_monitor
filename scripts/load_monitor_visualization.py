#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import csv

if __name__ == '__main__':
  with open('load_monitor.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    x = []
    y = []
    z = []
    cpu = []
    mem = []
    cpu_temp = []
    for row in csv_reader:
      x.append(float(row[0]))
      y.append(float(row[1]))
      z.append(float(row[2]))
      cpu.append(float(row[3]))
      mem.append(float(row[4]))
      cpu_temp.append(float(row[5]))
  
  fig, axs = plt.subplots(3)
  fig.suptitle("CPU MEM MONITOR")
  axs[0].set_title("CPU LOAD")
  img_cpu_load = axs[0].scatter(np.array(x), np.array(y), c=np.array(cpu))
  axs[1].set_title("MEMORY USAGE")
  img_mem_usage = axs[1].scatter(np.array(x), np.array(y), c=np.array(mem))
  axs[2].set_title("CPU TEMPERATURE")
  img_cpu_temp = axs[2].scatter(np.array(x), np.array(y), c=np.array(cpu_temp))
  plt.colorbar(img_cpu_load, label='Cpu Load', ax=axs[0])
  plt.colorbar(img_mem_usage, label='Mem Usage', ax=axs[1])
  plt.colorbar(img_cpu_temp, label='Cpu Temp', ax=axs[2])

  plt.show()
  