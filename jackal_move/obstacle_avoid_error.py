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
        self.pub = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
        
    def scan_callback(self, msg):
        self.scaner = msg

    def obs_avoid(self):
        if self.index_laser>=0 and self.index_laser<=240:
            print('Right Setor')
            
            vel_msg = Twist()

            # Receiveing the user's input
            speed = 20
            angle = 15
            if self.index_laser>=0 and self.index_laser<=240:
                clockwise = False
            else:
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

    def front(self):
        rate = rospy.Rate(10)

        #criando a menssagem twist
        move_cmd = Twist()
        move_cmd.linear.x = 10

        # For the next 6 seconds publish cmd_vel move commands to Turtlesim
        while self.index_laser<=300 or self.index_laser>=350:
            #while self.obstaculo>=1:
            rospy.loginfo(move_cmd)
            self.pub.publish(move_cmd)
            rate.sleep() 
        self.sensor_data()
    
    '''def sensor_data(self):
        print('iniciando sensor lidar')
        data = self.scaner.ranges #pega o vetor com as infos de distancia
        #print(self.scaner.ranges)
        print(data)
        #obstaculo = np.min(data)
        #print('menor leitura', obstaculo)
        #self.index_laser = self.scaner.ranges.index(min(self.scaner.ranges))
        #print('laser:', self.index_laser)'''

    def move(self):
        #rospy.sleep(3)
        #self.sensor_data()
        #while not rospy.is_shutdown():
        while 1:            
            #while self.index_laser<=240:
            #self.sensor_data()
            data = self.scaner.ranges #pega o vetor com as infos de distancia
            #print(data)
            obstaculo = min(data)
            #print('menor leitura', obstaculo)
            index_laser = data.index(obstaculo)
            print('laser:', index_laser)
            
            #SETORES
            #front #241 a 480
            '''
            if self.index_laser<=300 or self.index_laser>=350:
                 #while self.obstaculo>=1:
                self.front()

            #right
            elif self.index_laser>=0 and self.index_laser<=299:
                print('Chamando a funcao right_avoid')
                self.right_avoid(self.index_laser)
                #self.front(self.index_laser)
            
            #left
            elif self.index_laser>=351 and self.index_laser<=720:
                print('Chamando a funcao left_avoid')
                self.left_avoid(self.index_laser)
                #self.front(self.index_laser)
            
            else:
                self.front()
        
        #self.sensor_data()
        #self.front(self.index_laser)
        '''
        #self.rate.sleep()

rospy.init_node('random_jackal_commands', anonymous=True)

nav = JackalNav()
nav.move()