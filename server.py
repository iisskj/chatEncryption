# server.py
import socket
import threading

clients = []

def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                print(f"转发消息: {msg}")
                for c in clients:
                    if c != client_socket:
                        try:
                            c.send(msg.encode('utf-8'))
                        except:
                            c.close()
                            clients.remove(c)
            else:
                break
        except:
            break
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((config.SERVER_IP, config.PORT))
    server.listen(5)
    print(f"服务器启动，监听 {config.SERVER_IP}:{config.PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"连接来自 {addr}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    import config
    start_server()
