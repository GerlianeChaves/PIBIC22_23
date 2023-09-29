import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class JackalNav:
    def __init__(self): #executa so uma vez e fica salvo

        # BRUTE DATAS
        self.rate = rospy.Rate(10)
        self.scaner = LaserScan() 
    
        # SUBSCRIBER
        
        # SENSOR LASER SCAN
        self.scan_sub = rospy.Subscriber("/front/scan", LaserScan, self.scan_callback)
        
    def scan_callback(self, msg):
        self.scaner = msg

    def teste(self):
        rospy.sleep(3)
        while 1:
            rang = self.scaner.ranges
            ang = self.scaner.angle_increment
            ang_inicial = self.scaner.angle_min
            a = ang_inicial+np.argmin(rang)*ang
            print(np.rad2deg(a))
            self.rate.sleep()

rospy.init_node('random_jackal_commands', anonymous=True)

nav = JackalNav()
nav.teste()