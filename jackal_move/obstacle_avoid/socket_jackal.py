import socket

# Definir o IP e a porta do ambiente do Colab
IP = '10.0.0.106'  # Substitua pelo IP do Colab
PORT = 8888        # A mesma porta definida no servidor

# Criar o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# Enviar mensagem para o servidor no Colab
message = "Olá, Colab!"
client_socket.send(message.encode())

client_socket.close()
