import serial
import time

ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)
print("按 Enter 亮灯，再按 Enter 灭灯，输入 q 退出")

while True:
    cmd = input(">>> ")
    if cmd == 'q':
        break
    elif cmd == '':
        ser.write(b'1')
        time.sleep(0.5)
        ser.write(b'0')

ser.close()
print("测试结束。")