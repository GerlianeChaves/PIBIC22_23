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
        self.pub = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
        self.velocity_publisher = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
 
    def scan_callback(self, msg):
        self.scaner = msg

    def sensor_data(self):
        self.data = self.scaner.ranges #pega o vetor com as infos de distancia
        #print(data)
        self.obstaculo = min(self.data)
        print('obstaculo', self.obstaculo)
        self.index_laser = self.data.index(self.obstaculo)
        print('laser:', self.index_laser)
        #print(self.scaner.angle_increment)
    
    def setor(self):
        #SETORES
        self.behindr_setor = self.data[0:120]
        self.right_setor = self.data[120:280]
        self.front_setor = self.data[280:440]
        self.left_setor = self.data[440:600]
        self.behindl_setor = self.data[600:720]

        print('brs', self.behindr_setor)
        print('rs',self.right_setor)
        print('fs',self.front_setor)
        print('ls',self.left_setor)
        print('bls',self.behindl_setor)
    
    def front(self):
        print('iniciando front')
        rate = rospy.Rate(10)

        #criando a menssagem twist
        move_cmd = Twist()
        move_cmd.linear.x = 0.5

        # For the next 6 seconds publish cmd_vel move commands to Turtlesim
        #if self.index_laser<=280 or self.index_laser>440:
        if min(self.data[280:440]) >= 0.3:
            print('obstaculo frente:', min(self.data[280:440]) )
            rospy.loginfo(move_cmd)
            self.pub.publish(move_cmd)
            print('andando')
            rate.sleep()

        print('terminou frente')
        self.sensor_data()
    
    def reverse(self):
        print('iniciando reverse')
        rate = rospy.Rate(10)

        #criando a menssagem twist
        move_cmd = Twist()
        move_cmd.linear.x = -2
        # For the next 6 seconds publish cmd_vel move commands to Turtlesim
        if min(self.data[280:440])<=0.23:
            print('obstaculo re: ', min(self.data[280:440]))
            rospy.loginfo(move_cmd)
            self.pub.publish(move_cmd)
            print('dando re')
            rate.sleep() 
        print('re finalizada')
        self.sensor_data()

    def obs_avoid(self):
        print('Iniciando desvio')
        vel_msg = Twist()

        # Receiveing the user's input
        speed = 10
        angle = 90
        #clockwise = False
        print('desviando')
        
        if min(self.data[120:280]) < min(self.data[440:600]):
            print('obstaculo lateral mais proximo na direta, desviando pra esquerda')
            clockwise = False
        else:
            print('obstaculo lateral mais proximo na esquerda, desviando pra direita')
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

        #while(current_angle < relative_angle):
        while min(self.data[280:440]) == self.obstaculo:
            if min(self.data[280:440]) <=0.23:
                print('obstaculo na frente: ', min(self.data[280:440])) 
                print('obstaculo mais proximo', min(self.data))
                self.velocity_publisher.publish(vel_msg)
                t1 = rospy.Time.now().to_sec()
                current_angle = angular_speed*(t1-t0)

        #Forcing our robot to stop
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        print('desviou')
        rospy.sleep(3)
        self.sensor_data()

    def move(self):
        rospy.sleep(3)
        while not rospy.is_shutdown():
            self.sensor_data()
                     
            #if self.index_laser>=280 and self.index_laser<=440:
            '''
            if self.obstaculo == min(self.data[280:440]):
                if min(self.data[280:440]) >=0.23:
                    self.front()
                else:
                    self.reverse()
                    self.obs_avoid()
                #self.setor()
            '''
            if self.index_laser<280 or self.index_laser>440:
                self.front()
            #else:
                #self.reverse()

        self.rate.sleep()

rospy.init_node('random_jackal_commands', anonymous=True)

nav = JackalNav()
nav.move()