import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class JackalNav:
    def __init__(self): #executa so uma vez e fica salvo

        # BRUTE DATAS
        self.rate = rospy.Rate(10)
        self.cam = Image()
    
        # camera
        self.cam_sub = rospy.Subscriber("/front/image_raw", Image, self.cam_callback)
            
    def cam_callback(self, msg):
        #self.cam = msg.data
        self.cam = msg

        # Acessar os campos da mensagem

    def image_callback(self, msg):
        bridge = CvBridge()
        try:
            # Converter a mensagem de imagem para uma imagem OpenCV
            cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # Aplicar algum processamento na imagem
            # Por exemplo, converter para escala de cinza
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Exibir a imagem processada
            cv2.imshow("Processed Image", gray_image)
            cv2.waitKey(1)
        except Exception as e:
            rospy.logerr(e)

    def camera_info(self): 
        rospy.sleep(3)
        #while not rospy.is_shutdown():
        print(self.cam)
    
    def cam_show(self):
        rospy.sleep(3)
        while not rospy.is_shutdown():
            self.camera_info()

rospy.init_node('random_jackal_commands', anonymous=True)
nav = JackalNav()
rospy.Subscriber("/front/image_raw", Image, nav.image_callback)
rospy.spin()