# server.py - 低资源占用版
import socket
import select
import encrypt

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    server.setblocking(False)  # 非阻塞
    print("🌐 服务器启动（低资源模式）...")

    clients = []
    inputs = [server]

    while True:
        # select 等待有数据可读的 socket
        readable, _, _ = select.select(inputs, [], [], 0.1)  # 超时 100ms

        for sock in readable:
            if sock is server:
                # 新连接
                conn, addr = server.accept()
                conn.setblocking(False)
                inputs.append(conn)
                clients.append(conn)
                print(f"✅ {addr} 加入")
            else:
                # 接收消息
                try:
                    data = sock.recv(2048)
                    if data:
                        # 转发给其他客户端
                        for client in clients:
                            if client != sock:
                                try:
                                    client.send(data)
                                except:
                                    client.close()
                                    inputs.remove(client)
                                    clients.remove(client)
                    else:
                        # 客户端断开
                        inputs.remove(sock)
                        clients.remove(sock)
                        sock.close()
                except:
                    pass  # 忽略异常，避免忙循环

        # 可在此处加空闲任务或日志
        # time.sleep(0.001)  # 可选：进一步降低 CPU

if __name__ == "__main__":
    start_server()
