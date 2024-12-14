import os
import sys
import threading
from time import sleep
import socketio

# 创建 SocketIO 客户端实例
sio = socketio.Client()

namespace = "/bmc"

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


# 对 host 进行上电
@sio.on("power_on", namespace=namespace)
def on_certify():
    print(f"Received power on command")

    # TODO: 进行上电


# 对 host 进行下电
@sio.on("power_off", namespace=namespace)
def on_certify():
    print(f"Received power off command")

    # TODO: 进行下电


# 对 host 进行下电
@sio.on("reboot", namespace=namespace)
def on_certify():
    print(f"Received reboot command")

    # TODO: 重启 —— 则先下电再上电，操作间隔可以设置为5s?


def main():
    try:
        # TODO: 拿到 host 的 identity, 不要再单独生成一个了

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
