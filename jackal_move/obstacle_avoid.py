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

        self.velocity_publisher = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
        
    def scan_callback(self, msg):
        self.scaner = msg

    def right_avoid(self, index_laser):
        if index_laser>=0 and index_laser<=240:
            print('Right Setor')
            
            vel_msg = Twist()

            # Receiveing the user's input
            speed = 20
            angle = 45
            clockwise = False

            #Converting from angles to radians
            angular_speed = speed*2*3.1415926535897/360
            relative_angle = angle*2*3.1415926535897/360

            #We wont use linear components
            vel_msg.linear.x=0
            vel_msg.linear.y=0
            vel_msg.linear.z=0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0

            if clockwise:
                vel_msg.angular.z = -abs(angular_speed)
            else:
                vel_msg.angular.z = abs(angular_speed)

            # Setting the current time for distance calculus
            t0 = rospy.Time.now().to_sec()
            current_angle = 0

            while(current_angle < relative_angle):
                self.velocity_publisher.publish(vel_msg)
                t1 = rospy.Time.now().to_sec()
                current_angle = angular_speed*(t1-t0)

            #Forcing our robot to stop
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
            rospy.sleep(3)

    
    def left_avoid(self, index_laser):
        if index_laser>=481 and index_laser<=720:
            print('Left Setor')

            vel_msg = Twist()

            # Receiveing the user's input
            speed = 20
            angle = 45
            clockwise = True

            #Converting from angles to radians
            angular_speed = speed*2*3.1415926535897/360
            relative_angle = angle*2*3.1415926535897/360

            #We wont use linear components
            vel_msg.linear.x=0
            vel_msg.linear.y=0
            vel_msg.linear.z=0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0

            if clockwise:
                vel_msg.angular.z = -abs(angular_speed)
            else:
                vel_msg.angular.z = abs(angular_speed)

            # Setting the current time for distance calculus
            t0 = rospy.Time.now().to_sec()
            current_angle = 0

            while(current_angle < relative_angle):
                self.velocity_publisher.publish(vel_msg)
                t1 = rospy.Time.now().to_sec()
                current_angle = angular_speed*(t1-t0)

            #Forcing our robot to stop
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
            rospy.sleep(3)


    def move(self):
        
        rospy.sleep(3)
        while 1:
            data = self.scaner.ranges #pega o vetor com as infos de distancia
            #print(data)
            obstaculo = min(data)
            #print('menor leitura', obstaculo)
            index_laser = data.index(obstaculo)
            print('laser:', index_laser)

            #SETORES
            #right
            if index_laser>=0 and index_laser<=240:
                print('Chamando a funcao right_avoid')
                self.right_avoid(index_laser)
            
            #front
            if index_laser>=241 and index_laser<=480:
                print('Chamando a funcao front_avoid')

            #left
            if index_laser>=481 and index_laser<=720:
                print('Chamando a funcao left_avoid')
                self.left_avoid(index_laser)

            self.rate.sleep()

rospy.init_node('random_jackal_commands', anonymous=True)

nav = JackalNav()
nav.move()