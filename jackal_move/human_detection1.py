import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class JackalPersonDetection:
    def __init__(self):
        rospy.init_node('jackal_person_detection')

        # Inicialização do CvBridge
        self.bridge = CvBridge()
        
        # Variável de controle para verificar se a primeira imagem já foi processada
        self.first_image_processed = False
        
        # Inscrição no tópico da câmera
        self.camera_sub = rospy.Subscriber('/front/image_raw', Image, self.image_callback)

    def image_callback(self, msg):
        if self.first_image_processed:
            return
        
        try:
            # Converter a mensagem de imagem para uma imagem OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

            # Redimensionar a imagem para um tamanho menor
            scale_percent = 50  # Reduzir para 50% do tamanho original
            width = int(cv_image.shape[1] * scale_percent / 100)
            height = int(cv_image.shape[0] * scale_percent / 100)
            resized_image = cv2.resize(cv_image, (width, height))

            # Carregar o modelo YOLO pré-treinado para detecção de pessoas
            print('Carregando modelos')
            net = cv2.dnn.readNetFromDarknet('yolov3_new.cfg', 'yolov3_new.weights')
            print('Modelos carregados')
            
            # Carregar as classes
            classes = []
            with open('coco.names', 'r') as f:
                classes = [line.strip() for line in f.readlines()]

            # Obter informações da imagem
            height, width, _ = cv_image.shape

            # Normalizar a imagem e convertê-la em um blob
            blob = cv2.dnn.blobFromImage(cv_image, 1/255.0, (416, 416), swapRB=True, crop=False)

            # Definir a entrada da rede neural
            net.setInput(blob)

            # Executar a detecção
            outputs = net.forward(net.getUnconnectedOutLayersNames())

            # Configurar parâmetros de confiança e supressão de não-máxima para filtrar detecções
            confidence_threshold = 0.5
            nms_threshold = 0.4

            # Listas para armazenar resultados
            boxes = []
            confidences = []
            class_ids = []

            # Iterar sobre todas as saídas
            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = scores.argmax()
                    confidence = scores[class_id]

                    if confidence > confidence_threshold and class_id == 0:  # Classe 0 = Pessoa
                        # Escalar as coordenadas da caixa delimitadora para as dimensões da imagem original
                        box = detection[0:4] * np.array([width, height, width, height])
                        (center_x, center_y, box_width, box_height) = box.astype("int")

                        # Calcular as coordenadas (x, y) do canto superior esquerdo da caixa delimitadora
                        x = int(center_x - (box_width / 2))
                        y = int(center_y - (box_height / 2))

                        # Adicionar a caixa delimitadora, confiança e ID da classe às listas
                        boxes.append([x, y, int(box_width), int(box_height)])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # Aplicar a supressão de não-máxima para eliminar detecções redundantes
            indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

            # Desenhar as caixas delimitadoras e exibir informações na imagem
            font = cv2.FONT_HERSHEY_SIMPLEX
            if len(indices) > 0:
                for i in indices.flatten():
                    box = boxes[i]
                    x, y, w, h = box
                    label = '{}: {:.2f}'.format(classes[class_ids[i]], confidences[i])
                    cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(cv_image, label, (x, y - 5), font, 0.5, (0, 255, 0), 1)

            # Exibir a imagem com as detecções
            cv2.imshow('Jackal Person Detection', cv_image)
            cv2.waitKey(1)

            self.first_image_processed = True

        except Exception as e:
            rospy.logerr(e)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        jackal_detection = JackalPersonDetection()
        jackal_detection.run()
    except rospy.ROSInterruptException:
        pass
