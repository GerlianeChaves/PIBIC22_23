import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def __init__(self, right_avoid): #executa so uma vez e fica salvo

    # BRUTE DATAS
    self.rate = rospy.Rate(10)
    self.scaner = LaserScan() 

    # SUBSCRIBER
    
    # SENSOR LASER SCAN
    self.scan_sub = rospy.Subscriber("/front/scan", LaserScan, self.scan_callback)
        
def scan_callback(self, msg):
    self.scaner = msg

def right_avoid(self, index_laser):
    if index_laser>=0 and index_laser<=240:
        print('Right Setor')
        
        rospy.init_node('random_jackal_commands', anonymous=True)
        velocity_publisher = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)
        vel_msg = Twist()

        # Receiveing the user's input
        speed = 10
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

        # Checking if our movement is CW or CCW
        if clockwise:
            vel_msg.angular.z = -abs(angular_speed)
        else:
            vel_msg.angular.z = abs(angular_speed)

        # Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        while(current_angle < relative_angle):
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed*(t1-t0)

        #Forcing our robot to stop
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        rospy.spin()

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
            print('Chamando a funcao desvio da direita')
            right_avoid()
        
        #front
        if index_laser>=241 and index_laser<=480:
            print('Front Setor')

        #left
        if index_laser>=481 and index_laser<=720:
            print('Left Setor')

        self.rate.sleep()

rospy.init_node('random_jackal_commands', anonymous=True)

if __name__ == '__main__':
    while not rospy.is_shutdown():
        data = self.scaner.ranges #pega o vetor com as infos de distancia
        #print(data)
        obstaculo = min(data)
        #print('menor leitura', obstaculo)
        index_laser = data.index(obstaculo)
        print('laser:', index_laser)

        #SETORES
        #right
        if index_laser>=0 and index_laser<=240:
            print('Chamando a funcao desvio da direita')
            right_avoid()
   
