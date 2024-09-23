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
    for row in csv_reader:
      x.append(float(row[0]))
      y.append(float(row[1]))
      z.append(float(row[2]))
      cpu.append(float(row[3]))
      mem.append(float(row[4]))
  plt.scatter(np.array(x), np.array(y), c=np.array(cpu))
  plt.colorbar(label='Cpu Load')
  plt.show()
  