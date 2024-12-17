import os
import sys
import threading
from time import sleep
import socketio
import subprocess

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

    command = "obmcutil poweron"
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )


# 对 host 进行下电
@sio.on("power_off", namespace=namespace)
def on_certify():
    print(f"Received power off command")

    command = "obmcutil chassisoff"
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )


# 对 host 进行下电
@sio.on("reboot", namespace=namespace)
def on_certify():
    print(f"Received reboot command")

    command_off = "obmcutil chassisoff"
    result = subprocess.run(
        command_off,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    sleep(5)
    command_on = "obmcutil poweron"
    result = subprocess.run(
        command_on,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


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
