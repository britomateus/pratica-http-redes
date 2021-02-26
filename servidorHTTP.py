# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTORES: MATEUS MEDEIROS DE ASSIS BRITO E ALICE MELO DE SOUSA
#
# SCRIPT: PRÁTICA HTTP
#

# importacao das bibliotecas
import socket

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print ('Serving HTTP on port %s ...' % PORT)

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    print (request.decode('utf-8'))

    request = request.decode('utf-8').split(" ")

    if(request[0] == 'GET'):
        if(request[1] == '/'):
            file = open('index.html')
            text = file.read()
            # declaracao da resposta do servidor
            http_response = "HTTP/1.1 200 OK\r\n\r\n" + text
        else:
            path = request[1][1:]
            try:
                file = open(path)
                text = file.read()
                # declaracao da resposta do servidor 
                http_response = "HTTP/1.1 200 OK\r\n\r\n" + text
            except:
                file = open('404_not_found_page.html')
                text = file.read()
                # declaracao da resposta do servidor 
                http_response = "HTTP/1.1 404 NOT FOUND\r\n\r\n" + text
    else:
        file = open('400_bad_request_page.html')
        text = file.read() 
        # declaracao da resposta do servidor
        http_response = "HTTP/1.1 400 BAD REQUEST\r\n\r\n" + text

    
    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(http_response.encode('utf-8'))
    # encerra a conexao
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()