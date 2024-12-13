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

    # TODO: 生成 shared_key 逻辑
    shared_key = "xxxxxxx"
    context["shared_key"] = shared_key

    # 发送(必须等到建立连接后再能成功发送)
    connect_event.wait()
    sio.emit("receive_shared_key", shared_key, namespace="/host")


# 进行可信校验, 向服务端发送 log 文件
@sio.on("certify", namespace=namespace)
def on_certify():
    print(f"Received certify command")

    # TODO: 修改 log 文件路径
    file_path = "./log1.txt"
    up_load_log_file("certify", file_path)


# 更新基准值, 向服务端发送 log 文件
@sio.on("update_base", namespace=namespace)
def on_certify():
    print(f"Received update base command")

    # TODO: 修改 log 文件路径
    file_path = "./log1.txt"
    up_load_log_file("update_base", file_path)


def up_load_log_file(op: str, file_path: str):
    # 发送(必须等到建立连接后再能成功发送)
    connect_event.wait()

    try:
        with open(file_path, "rb") as f:
            file_name = file_path.split("/")[-1]
            # TODO: 使用 shared_key 对文件内容进行加密
            shared_key = context["shared_key"]
            file_content = f.read()

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
    try:
        # TODO: 拿到 xxxaaabbb

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
