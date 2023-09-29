import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from lidar_sensor import sensor_data

def front(self):
    rate = rospy.Rate(10)

    #criando a menssagem twist
    move_cmd = Twist()
    move_cmd.linear.x = 10

    # For the next 6 seconds publish cmd_vel move commands to Turtlesim
    while self.index_laser<=300 or self.index_laser>=350:
        #while self.obstaculo>=1:
        if self.obstaculo>=1:
            rospy.loginfo(move_cmd)
            self.pub.publish(move_cmd)
            rate.sleep() 
    self.sensor_data()
    pass

def obs_avoid(self, index_laser):
    if index_laser>=0 and index_laser<=240:
        print('Right Setor')
        
        vel_msg = Twist()

        # Receiveing the user's input
        speed = 20
        angle = 15
        if index_laser>=0 and index_laser<=240:
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
        pass