# coding=utf-8
import os
import sys
import threading
import hmac
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from time import sleep
import socketio

# 创建 SocketIO 客户端实例
sio = socketio.Client()

namespace = "/host"

context = {}

connect_event = threading.Event()


def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ciphertext  # 返回 IV 和密文


def aes_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]  # 提取 IV
    ciphertext = encrypted_data[16:]  # 提取密文
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data


# 连接成功时的回调函数
@sio.on("connect", namespace=namespace)
def connect():
    print("Connect with server")
    connect_event.set()


# 连接失败时的回调函数
@sio.on("connect_error", namespace=namespace)
def connect_error(data):
    print(f"Connect error: {data}")


# 断开连接时的回调函数
@sio.on("disconnect", namespace=namespace)
def disconnect():
    print("Disconnect with server")


# 接收服务端传来的random_key, 向服务端发送host端的 key
@sio.on("random_key", namespace=namespace)
def on_random_key(data):
    print(f"Received random key: {data}")
    context["random_key"] = data

    cert = "trusted.cert"
    hmac_key = hmac.new(cert, random_number, digestmod="SHA256").hexdigest()
    shared_key = hmac_key[:16]
    context["shared_key"] = shared_key

    # 发送(必须等到建立连接后再能成功发送)
    connect_event.wait()
    sio.emit("receive_shared_key", shared_key, namespace="/host")


# 进行可信校验, 向服务端发送 log 文件
@sio.on("certify", namespace=namespace)
def on_certify():
    print(f"Received certify command")

    file_path = "/sys/kernel/security/ima/ascii_runtime_measurements"
    up_load_log_file("certify", file_path)


# 更新基准值, 向服务端发送 log 文件
@sio.on("update_base", namespace=namespace)
def on_certify():
    print(f"Received update base command")

    file_path = "/sys/kernel/security/ima/ascii_runtime_measurements"
    up_load_log_file("update_base", file_path)


def up_load_log_file(op: str, file_path: str):
    # 发送(必须等到建立连接后再能成功发送)
    connect_event.wait()

    try:
        with open(file_path, "rb") as f:
            file_name = file_path.split("/")[-1]
            # 使用 shared_key 对文件内容进行加密
            shared_key = context["shared_key"]
            file_content = f.read()
            file_to_cipher = file_content.encode()
            iv = encrypted_data[:16]  # 提取 IV
            ciphertext = encrypted_data[16:]  # 提取密文
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
            # 发送文件数据到服务端
            sio.emit(
                "receive_certify_log",
                {"op": op, "file_name": file_name, "file_content": file_content},
                namespace=namespace,
            )
            print(f"File {file_name} sent to server.")

    except FileNotFoundError:
        sio.emit(
            "receive_certify_log",
            {"op": op, "error": "log file not found"},
            namespace=namespace,
        )
        print(f"File not found: {file_path}")


def main():
    # while True:
    try:
        file = open("/etc/trusted/trusted.cert")
        ident = file.read()
        hashres = str(hash(ident))
        headers = {"identity": hashres}
        sio.connect(f"http://10.31.94.100:5000", namespaces=["/host"], headers=headers)
        context["first_connect"] = True
        file.close()
        sio.wait()

    except KeyboardInterrupt:
        sio.disconnect()
    except Exception as e:
        print(f"Connect exception: {e}")
    # finally:
    #     continue


if __name__ == "__main__":
    main()
