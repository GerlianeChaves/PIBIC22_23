import cv2
import numpy as np

# Carregar o modelo Darknet
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Converter o modelo para o formato ONNX
output_model = 'yolov3_convert.onnx'
net.save(output_model)
print("Modelo convertido para {}".format(output_model))

