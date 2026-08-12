import serial
import time

# ==================== 连接 Arduino ====================
PORT = 'COM4'          # 改成你的实际端口
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print(f"✅ 已连接 Arduino（{PORT}）")
print("桌面电子琴 - 系统启动")
print("=" * 50)
print("按下不同按钮，蜂鸣器发出不同音调")
print("Python 端实时显示当前弹奏的音符")
print("按 Ctrl+C 退出")
print("=" * 50 + "\n")

# ==================== 主循环 ====================
try:
    while True:
        if ser.in_waiting > 0:
            note = ser.readline().decode('utf-8').strip()
            if note in ["Do", "Re", "Mi", "Fa", "Sol"]:
                # 不同音符配不同 emoji
                emoji_map = {
                    "Do": "🔴", "Re": "🟠", "Mi": "🟡",
                    "Fa": "🟢", "Sol": "🔵"
                }
                emoji = emoji_map.get(note, "🎵")
                print(f"\r当前弹奏：{emoji} {note}  ", end='')

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\n电子琴关闭。")
    ser.close()
    print("程序结束。")