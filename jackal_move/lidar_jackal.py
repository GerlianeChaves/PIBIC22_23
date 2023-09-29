import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import random 

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

    def move(self):
        rospy.sleep(3)
        while 1:
            data = self.scaner.ranges #pega o vetor com as infos de distancia
            print(data)
            obstaculo = min(data)
            print('menor leitura', obstaculo)
            index_laser = data.index(obstaculo)
            print('lase:', index_laser)
            if obstaculo>=200 or obstaculo<=300:
                pub = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
            # Essa linha inidica em qual no sera publicado, no caso /jackal_velocity_controller/cmd_vel, o tipo de mensagem: Twist e a taxa de mensagens enviadas (10)

                rospy.init_node('random_jackal_commands', anonymous=True)
            # Essa linha inicia o no e nomea-lo da forma como queremos (random_jackal_commands)
            # anonymous=True e utilizado apenas para tornar o nome do no unico, ele adiciona numeros ao final dele para ser sempre unico

                rate = rospy.Rate(10)

            #criando a menssagem twist
                move_cmd = Twist()
                move_cmd.linear.x = 1 #random.randint(0, 10)

                # For the next 6 seconds publish cmd_vel move commands to Turtlesim
                while not rospy.is_shutdown():
                    #print('Teste6')
                        rospy.loginfo(move_cmd)
                        pub.publish(move_cmd)
                        rate.sleep() 

            self.rate.sleep()

rospy.init_node('random_jackal_commands', anonymous=True)

nav = JackalNav()
nav.move()