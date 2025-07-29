# client.py（更新版）

import socket
import threading
import config
import encrypt
import random
import time

# 客户端使用一个固定本地端口范围（避免冲突）
LOCAL_PORT = random.randint(1001, 1030)  # 模拟“端口标识”

def receive_messages(client_socket):
    while True:
        time.sleep(0.01)
        try:
            encrypted_msg = client_socket.recv(2048).decode('utf-8', errors='ignore')
            if not encrypted_msg:
                break
            # 解密
            decrypted_msg = encrypt.decrypt(encrypted_msg)
            print(f"\n[消息] {decrypted_msg}")
        except:
            print("\n连接断开")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定本地端口（仅用于标识，不强制监听）
    try:
        client_socket.bind(('', LOCAL_PORT))  # 使用随机本地端口
    except:
        pass  # 如果端口被占用，系统自动分配也没关系

    try:
        client_socket.connect((config.SERVER_IP, config.PORT))
    except:
        print("无法连接到服务器，请检查 IP 和网络")
        return

    print(f"✅ 已连接到聊天服务器！你的端口标识: @{LOCAL_PORT}")
    print("输入消息开始聊天（输入 'quit' 退出）")

    # 启动接收线程
    thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    thread.start()

    # 主线程发送消息
    while True:
        msg = input()
        if msg.lower() == 'quit':
            break

        # ✅ 在原始消息前加上端口标识
        tagged_msg = f"@{LOCAL_PORT}: {msg}"

        # 加密后发送
        encrypted_msg = encrypt.encrypt(tagged_msg)
        client_socket.send(encrypted_msg.encode('utf-8'))
        time.sleep(0.05)

    client_socket.close()
    print("已退出")

if __name__ == "__main__":
    start_client()
