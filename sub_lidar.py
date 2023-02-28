import rospy
from sensor_msgs.msg import LaserScan

class JackalLaser():
    def __init__(self):
        self.laser_data = LaserScan()
        self.rate = rospy.Rate(10)

        self.laser_sub = rospy.Subscriber('/front/scan', LaserScan,self.laser_callback)
    
    def laser_callback(self, msg):
        self.laser_data = msg
    
    def print_laser(self):
        while True:
            print(self.laser_data.ranges)
            print('='*40)
            self.rate.sleep()

rospy.init_node('jackal_test')

jackal = JackalLaser()
jackal.print_laser()