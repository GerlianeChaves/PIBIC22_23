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
            data = self.scaner.ranges #pega o vetor com as infos de distancia
            #print(data)
            obstaculo = min(data)
            #print('menor leitura', obstaculo)
            index_laser = data.index(obstaculo)
            print('laser:', index_laser)
            print(self.scaner.angle_increment)

            #SETORES
            #behind_right
            if index_laser>=0 and index_laser<120:
                print('Behind Right Setor')
            #right
            if index_laser>=120 and index_laser<280:
                print('Right Setor')
            
            #front
            if index_laser>=280 and index_laser<440:
                print('Front Setor')

            #left
            if index_laser>=440 and index_laser<600:
                print('Left Setor')

            #behind_left
            if index_laser>=600 and index_laser<=720:
                print('Behind Left Setor')

            self.rate.sleep()

rospy.init_node('random_jackal_commands', anonymous=True)

nav = JackalNav()
nav.teste()