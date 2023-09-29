import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

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
            
    def camera_info(self): 
        rospy.sleep(3)
        #while not rospy.is_shutdown():
        '''
        self.cam.header.stamp = rospy.Time.now()  # Definir o timestamp
        self.cam.height = 480  # Definir a altura da imagem
        self.cam.width = 640  # Definir a largura da imagem
        self.cam.encoding = "rgb8"  # Definir a codificacao da imagem
        self.cam.step = self.cam.width * 3  # Definir o numero de bytes por linha (largura * 3 canais)
        self.cam.data = bytes([0] * (self.cam.width * self.cam.height * 3))  # Definir os dados da imagem (bytes)

        # Imprimir alguns campos da mensagem
        print("Altura da imagem:", self.cam.height)
        print("Largura da imagem:", self.cam.width)
        print("Codificacao da imagem:", self.cam.encoding)
        #print(self.cam)
        img = len(self.cam)
        print(img)
        '''
        print(self.cam)
    def cam_show(self):
        rospy.sleep(3)
        while not rospy.is_shutdown():
            self.camera_info()

rospy.init_node('random_jackal_commands', anonymous=True)
nav = JackalNav()
nav.cam_show()
