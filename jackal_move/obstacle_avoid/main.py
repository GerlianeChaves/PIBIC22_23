import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
#from avoid import front, avoid
from lidar_sensor import sensor_data

class JackalNav:
    def __init__(self): #executa so uma vez e fica salvo

        # BRUTE DATAS
        self.rate = rospy.Rate(10)
        self.scaner = LaserScan() 
    
        # SUBSCRIBER
        
        # SENSOR LASER SCAN
        self.index_laser = -1
        
        self.scan_sub = rospy.Subscriber("/front/scan", LaserScan, self.scan_callback)

        self.velocity_publisher = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)

        self.pub = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
        
    def scan_callback(self, msg):
        self.scaner = msg

    def sensor_data(self):
        print('iniciando sensor lidar')
        data = self.scaner.ranges #pega o vetor com as infos de distancia
        print(data)
        self.obstaculo = min(data)
        print('menor leitura', self.obstaculo)
        self.index_laser = data.index(self.obstaculo)
        print('laser:', self.index_laser)
    def move(self):
        while not rospy.is_shutdown():            
            sensor_data()
            
            #SETORES
            #front #241 a 480
            #if self.index_laser<=300 or self.index_laser>=350:
             #   self.front()
            #else:
             #   self.obs_avoid()
            
rospy.init_node('random_jackal_commands', anonymous=True)

nav = JackalNav()
nav.move()