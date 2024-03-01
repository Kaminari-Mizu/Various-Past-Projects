#importing necessary libraries
import socket
import select

#initiating header, IP, and port to be used
HEADERL = 10
IP = "192.168.1.105"#LAN "192.168.1.105"Local "127.0.0.1"#WAN"192.168.1.105"
PORT = 1555

#creating the socket object and initialising it
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

#function to allow server to receive messages from client
def receive_msg(client_socket):
    try:
        msg_header = client_socket.recv(HEADERL)

        if not len(msg_header):
            return False
        
        msg_length = int(msg_header.decode("utf-8").strip())
        return{"header": msg_header, "data": client_socket.recv(msg_length)}
    
    except:
        return False

#while loop allows server socket to remain open as long as messages can be sent and subsequently forward messages from one client to another
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_msg(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f"New connection accepted from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = receive_msg(notified_socket)

            if message is False:
                print(f"Connection closed from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
