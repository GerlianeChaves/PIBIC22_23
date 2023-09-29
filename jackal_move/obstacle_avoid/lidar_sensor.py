from main import scan_callback
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def sensor_data(self):
    print('iniciando sensor lidar')
    data = self.scaner.ranges #pega o vetor com as infos de distancia
    print(data)
    self.obstaculo = min(data)
    print('menor leitura', self.obstaculo)
    self.index_laser = data.index(self.obstaculo)
    print('laser:', self.index_laser)
    pass