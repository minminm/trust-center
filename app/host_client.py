import os
import sys
import threading
from time import sleep
import socketio

# 创建 SocketIO 客户端实例
sio = socketio.Client()

namespace = "/host"

context = {}

connect_event = threading.Event()


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

    # TODO: 生成 key 逻辑
    key = "xxxxxxx"

    # 发送(必须等到建立连接后再能成功发送)
    connect_event.wait()
    sio.emit("receive_key", key, namespace="/host")


# 进行可信校验, 向服务端发送 log 文件
@sio.on("certify", namespace=namespace)
def on_certify():
    print(f"Received certify command")

    # TODO: 调用框架, 得到日志
    file_path = "./log1.txt"

    # 发送(必须等到建立连接后再能成功发送)
    connect_event.wait()

    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
            file_name = file_path.split("/")[-1]

            # 发送文件数据到服务端
            sio.emit(
                "receive_certify_log",
                {"file_name": file_name, "file_content": file_content},
                namespace=namespace,
            )
            print(f"File {file_name} sent to server.")

    except FileNotFoundError:
        sio.emit(
            "receive_certify_log",
            {"error": "log file not found"},
            namespace=namespace,
        )
        print(f"File not found: {file_path}")


def main():
    try:
        headers = {"identity": "xxxaaabbb"}
        sio.connect(f"http://localhost:5000", namespaces=["/host"], headers=headers)
        context["first_connect"] = True
        sio.wait()

    except KeyboardInterrupt:
        sio.disconnect()
    except Exception as e:
        print(f"Connect exception: {e}")


if __name__ == "__main__":
    main()
