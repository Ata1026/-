import serial
import time

PORT = 'COM4'          # 改成你的端口号！
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)          # 等待 Arduino 初始化
print(f"✅ 已连接 {PORT}，按钮控制 LED (D9)，Ctrl+C 退出\n")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            raw = line.decode('utf-8').strip()
            
            if raw == '1':
                print("🔘 按下 -> 亮灯")
                ser.write(b'1')       # 发送亮灯命令
            elif raw == '0':
                print("⚪ 松开 -> 灭灯")
                ser.write(b'0')       # 发送灭灯命令
except KeyboardInterrupt:
    print("\n程序结束。")
    ser.close()