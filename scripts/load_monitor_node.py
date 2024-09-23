#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time

from nav_msgs.msg import Odometry

def readCpuInfo():
  f = open('/proc/stat')
  lines = f.readlines();
  f.close()
  for line in lines:
    line = line.lstrip()
    counters = line.split()
    if len(counters) < 5:
      continue
    if counters[0].startswith('cpu'):
      break
  total = 0
  for i in range(1, len(counters)):
    total = total + int(counters[i])
  idle = int(counters[4])
  return {'total':total, 'idle':idle}

def calcCpuUsage(counters1, counters2):
	idle = counters2['idle'] - counters1['idle']
	total = counters2['total'] - counters1['total']
	return 100 - (idle*100/total)

def getCpuUsage():
  counters1 = readCpuInfo()
  time.sleep(0.1)
  counters2 = readCpuInfo()
  return calcCpuUsage(counters1, counters2)

def readMemInfo():
  res = {'total':0, 'free':0, 'buffers':0, 'cached':0}
  f = open('/proc/meminfo')
  lines = f.readlines()
  f.close()
  i = 0
  for line in lines:
    if i == 4:
      break
    line = line.lstrip()
    memItem = line.lower().split()
    if memItem[0] == 'memtotal:':
      res['total'] = int(memItem[1])
      i = i +1
      continue
    elif memItem[0] == 'memfree:':
      res['free'] = int(memItem[1])
      i = i +1
      continue
    elif memItem[0] == 'buffers:':
      res['buffers'] = int(memItem[1])
      i = i +1
      continue
    elif memItem[0] == 'cached:':
      res['cached'] = int(memItem[1])
      i = i +1
      continue
  return res

def calcMemUsage(counters):
  used = counters['total'] - counters['free'] - counters['buffers'] - counters['cached']
  total = counters['total']
  return used*100/total

def getMemUsage():
  mem_usage = readMemInfo()
  return calcMemUsage(mem_usage)


class LoadMonitorNode(Node):
  def __init__(self):
    super().__init__('load_monitor_node')
    
    self.current_cpu_load = 0.0
    self.current_mem_load = 0.0
    self.current_odom = None
    self.prev_odom = None
    self.received_odom = False
    
    self.odom_sub = self.create_subscription(
      Odometry, "/localization/kinematic_state", self.OdomCallback, 5
    )
    timer_period = 1.0
    self.timer = self.create_timer(timer_period, self.timerCallback)
    
    self.file = open('load_monitor.csv', 'w')
    
  def OdomCallback(self, msg):
    if not self.received_odom:
      self.current_odom = msg
      self.received_odom = True
    else:
      self.prev_odom = self.current_odom
      self.current_odom = msg
          
  
  def timerCallback(self):
    if self.prev_odom is not None:
      prev_time = self.prev_odom.header.stamp.sec * 10e9 + self.prev_odom.header.stamp.nanosec
      current_time = self.current_odom.header.stamp.sec * 10e9 + self.current_odom.header.stamp.nanosec
      if (current_time-prev_time)*10e-9 > 1.0:
        return
    self.current_cpu_load = getCpuUsage()
    self.current_mem_load = getMemUsage()
    # write data
    self.file.write('{},{},{},{},{}\n'.format(
      self.current_odom.pose.pose.position.x, 
      self.current_odom.pose.pose.position.y, 
      self.current_odom.pose.pose.position.z,
      self.current_cpu_load,
      self.current_mem_load
      ))

  def __del__(self):
    self.file.close()

  
if __name__ == '__main__':
  rclpy.init()
  node = LoadMonitorNode()
  rclpy.spin(node)
  print("spin end!")
  node.destroy_node()
  rclpy.shutdown()