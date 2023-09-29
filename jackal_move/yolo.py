# Importar bibliotecas
import cv2
import numpy as np

# Carregar arquivos de configuracao
net = cv2.dnn.readNetFromDarknet('yolov3_new.cfg', 'yolov3_new.weights')

# Carregar classes
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Configurar caminho para a imagem de teste
# image_path = 'dad-gcce321c68_1280.jpg'
# image_path = 'humangazebo.png'
image_path = 'humangazebo1.jpeg'

# Carregar imagem
image = cv2.imread(image_path)

# Obter informacoes da imagem
height, width, _ = image.shape

# Normalizar a imagem e converte-la em um blob
blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)

# Definir entrada da rede neural
net.setInput(blob)

# Executar deteccao
outputs = net.forward(net.getUnconnectedOutLayersNames())

# Configurar parametros de confianca e sobreposicao para nao-maximum suppression
confidence_threshold = 0.5
nms_threshold = 0.4

# Listas para armazenar resultados
boxes = []
confidences = []
class_ids = []

# Iterar sobre todas as saidas
for output in outputs:
    for detection in output:
        # Obter pontuacoes de confianca e indice da classe com a maior pontuacao
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        # Filtrar deteccoes com confianca acima do limiar
        if confidence > confidence_threshold and class_id == 0:  # 0 e o indice da classe "pessoa"
            # Escalar as coordenadas da caixa delimitadora para as dimensoes da imagem original
            box = detection[0:4] * np.array([width, height, width, height])
            (center_x, center_y, box_width, box_height) = box.astype("int")

            # Calcular as coordenadas (x, y) do canto superior esquerdo da caixa delimitadora
            x = int(center_x - (box_width / 2))
            y = int(center_y - (box_height / 2))

            # Adicionar caixa delimitadora, confianca e ID da classe as listas
            boxes.append([x, y, int(box_width), int(box_height)])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Aplicar nao-maximum suppression para eliminar deteccoes redundantes
indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

# Desenhar caixas delimitadoras e exibir informacoes na imagem
font = cv2.FONT_HERSHEY_SIMPLEX
if len(indices) > 0:
    for i in indices.flatten():
        box = boxes[i]
        x, y, w, h = box
        #label = f'{classes[class_ids[i]]}: {confidences[i]:.2f}'
        label = '{}: {:.2f}'.format(classes[class_ids[i]], confidences[i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 5), font, 0.5, (0, 255, 0), 1)

# Exibir a imagem com as deteccoes
cv2.imshow('Imagem', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
