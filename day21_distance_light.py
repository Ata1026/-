import serial
import time

# ==================== 连接 Arduino ====================
PORT = 'COM4'          # 改成你的实际端口
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print(f"✅ 已连接 Arduino（{PORT}）")
print("距离感应调光灯 - 系统启动")
print("=" * 50)
print("手掌靠近超声波模块 → LED 变亮")
print("手掌远离 → LED 变暗")
print("按 Ctrl+C 退出")
print("=" * 50 + "\n")

# ==================== 主循环 ====================
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if ',' in line:
                parts = line.split(',')
                try:
                    distance = float(parts[0])
                    brightness = int(parts[1])
                except ValueError:
                    continue

                # 计算亮度百分比
                brightness_percent = int(brightness / 255 * 100)

                # 画距离进度条（0~50cm）
                bar_len = int(distance / 50 * 40)  # 40 个字符宽
                bar_len = max(0, min(40, bar_len))
                bar = "█" * bar_len + "░" * (40 - bar_len)

                # 画亮度进度条（0~100%）
                light_bar_len = brightness_percent // 2  # 50 个字符宽
                light_bar = "●" * light_bar_len + "○" * (50 - light_bar_len)

                # 根据距离给出文字提示
                if distance <= 10:
                    status = "🔴 很近"
                elif distance <= 25:
                    status = "🟡 中等"
                elif distance <= 50:
                    status = "🟢 较远"
                else:
                    status = "⚫ 超出范围"

                # 终端动态刷新显示
                print(f"\r距离:{distance:5.1f}cm |{bar}| {status}  "
                      f"亮度:{brightness:3d}({brightness_percent:3d}%) |{light_bar}|", end='')

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\n系统关闭。")
    ser.close()
    print("程序结束。")