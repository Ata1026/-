import serial
import time

PORT = 'COM4'
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print("舵机平滑半圈扫描开始...")

try:
    for i in range(0, 181, 2):   # 0, 5, 10, ..., 180
        ser.write(f"{i}\n".encode('utf-8'))
        time.sleep(0.1)              # 每隔 0.5 秒发一次
        # 读取 Arduino 反馈
        while ser.in_waiting > 0:
            print(f"\r{ser.readline().decode().strip()}",end="")


            
except KeyboardInterrupt:
    print("\n扫描中断。")

ser.close()
print("完成。")