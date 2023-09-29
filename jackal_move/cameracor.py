import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class JackalColorDetection:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/front/image_raw", Image, self.image_callback)

    def image_callback(self, msg):
        try:
            # Converter a mensagem de imagem para uma imagem OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # Converter a imagem para o espaco de cores desejado (por exemplo, HSV)
            hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            
            # Definir os intervalos de cor para a cor desejada (por exemplo, vermelho)
            lower_red = (0, 100, 100)
            upper_red = (30, 255, 255)
            
            # Aplicar uma mascara na imagem usando os intervalos de cor definidos
            mask = cv2.inRange(hsv_image, lower_red, upper_red)
            
            # Realizar operacoes de processamento de imagem para melhorar a deteccao
            blurred = cv2.GaussianBlur(mask, (5, 5), 0)
            
            # Encontrar contornos na imagem resultante
            contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Percorrer os contornos e identificar a cor detectada
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Definir um limite minimo de area para evitar deteccoes falsas
                    # Faca a acao desejada com base na deteccao da cor
                    
                    # Por exemplo, desenhe um retangulo ao redor do objeto detectado
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Exibir a imagem resultante
            cv2.imshow("Color Detection", cv_image)
            cv2.waitKey(1)
        
        except Exception as e:
            print('erro')
            rospy.logerr(e)

if __name__ == '__main__':
    rospy.init_node('jackal_color_detection')
    color_detection = JackalColorDetection()
