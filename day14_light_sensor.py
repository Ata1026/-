# 1. 导入需要的库
import serial   # 用于 Python 和 Arduino 通过 USB 串口通信
import time     # 用于延时等待

# ==================== 连接 Arduino ====================
PORT = 'COM4'          # Arduino 在你电脑上对应的串口号（去 Arduino IDE 工具→端口里看）
BAUD = 9600            # 波特率，必须和 Arduino 程序里 Serial.begin(9600) 一致

# 创建一个串口对象，用来和 Arduino 对话
ser = serial.Serial(PORT, BAUD, timeout=1)
# timeout=1 意思是：如果 1 秒内没收到数据，就不再死等，返回空

time.sleep(2)          # 等待 Arduino 复位完成（刚连上 USB 时 Arduino 会自动重启一次）
print(f"✅ 已连接 Arduino（{PORT}）")
print("智能夜灯系统启动")
print("=" * 50)
print("功能说明：")
print("  · 光线充足时，LED 熄灭")
print("  · 光线暗时，LED 自动亮起")
print("  · 电位器调节 LED 亮度（暗时有效）")
print("  · 按 Ctrl+C 退出")
print("=" * 50 + "\n")

# ==================== 主循环 ====================
try:
    while True:                          # 无限循环，一直运行，直到按下 Ctrl+C
        if ser.in_waiting > 0:           # 如果串口的接收缓冲区里有数据（说明 Arduino 发东西过来了）
            line = ser.readline()        # 读取一行数据，格式是 b'0,512\r\n'（字节串）
            raw = line.decode('utf-8').strip()  # 把字节串解码成普通字符串，并去掉末尾的换行符和回车符
            # 现在 raw 变成了类似 "0,512" 这样的字符串

            if ',' in raw:               # 确认数据里有逗号（防止读到空行或乱码）
                parts = raw.split(',')   # 用逗号把字符串切成两半（按逗号分割）
                # 比如 "0,512" → parts[0]="0", parts[1]="512"
                light = int(parts[0])    # 光敏模块的状态，0=明亮，1=很暗
                pot = int(parts[1])      # 电位器的读数，范围 0~1023

                # ---- 在终端显示状态 ----
                # 根据光线状态选择不同的 emoji 和文字
                light_status = "🌙 很暗" if light == 1 else "☀️ 明亮"

                # 把电位器读数转成百分比（0~100%）
                pot_percent = int(pot / 1023 * 100)

                # 画一条进度条：每 2% 用一个实心方块表示，总共 50 个方块
                bar_len = pot_percent // 2      # 需要多少个实心方块
                bar = "█" * bar_len + "░" * (50 - bar_len)  # 拼出完整的进度条

                # 打印到终端（\r 让光标回到行首，实现同一行不断刷新）
                print(f"\r光线:{light_status} | 电位器:{pot:4d}({pot_percent:3d}%) | {bar}", end='')

                # ---- 根据光线控制 LED ----
                if light == 1:      # 如果光敏模块判断为“暗”
                    ser.write(b'1') # 向 Arduino 发送字节 '1'（开灯命令）
                else:               # 如果光敏模块判断为“亮”
                    ser.write(b'0') # 向 Arduino 发送字节 '0'（关灯命令）

except KeyboardInterrupt:            # 如果用户按下 Ctrl+C（键盘中断异常）
    ser.write(b'0')                  # 先发送关灯命令，确保 LED 熄灭
    ser.close()                      # 关闭串口连接
    print("\n\n程序结束，LED 已关闭。")  # \n\n 是换行，让提示和之前的进度条分开