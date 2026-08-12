import serial
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time

# ==================== 连接 Arduino ====================
PORT = 'COM4'
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print(f"✅ 已连接 Arduino（{PORT}）")
print("智能温控风扇系统启动\n")

# ==================== 数据存储（最近 50 个数据点） ====================
history_len = 50
time_axis = deque(np.linspace(-49, 0, history_len), maxlen=history_len)
current_temp_history = deque([0] * history_len, maxlen=history_len)
target_temp_history = deque([0] * history_len, maxlen=history_len)
time_counter = 0

# ==================== 设置实时绘图 ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

plt.ion()  # 开启交互模式
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# ---- 子图1：温度曲线 ----
line_current, = ax1.plot([], [], 'r-', linewidth=2, label='当前温度')
line_target, = ax1.plot([], [], 'b--', linewidth=2, label='目标温度')
ax1.set_ylim(0, 50)
ax1.set_xlim(-50, 0)
ax1.set_ylabel("温度 (°C)")
ax1.set_title("智能温控风扇 - 实时温度监控")
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# ---- 子图2：风扇转速 ----
fan_speed_bar = ax2.barh(['风扇转速'], [0], color='orange', height=0.5)[0]
ax2.set_xlim(0, 180)
ax2.set_xlabel("舵机角度 (°)")
ax2.set_title("风扇转速")

plt.tight_layout()
plt.show()

# ==================== 主循环 ====================
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if ',' in line:
                parts = line.split(',')
                try:
                    current = float(parts[0])
                    target = float(parts[1])
                except ValueError:
                    continue

                # 更新数据
                time_counter += 1
                time_axis.append(time_counter)
                current_temp_history.append(current)
                target_temp_history.append(target)

                # 更新曲线
                line_current.set_data(list(time_axis), list(current_temp_history))
                line_target.set_data(list(time_axis), list(target_temp_history))
                ax1.set_xlim(time_counter - 50, time_counter)

                # 更新风扇转速柱状图
                if current > target:
                    speed = min(180, (current - target) * 9)  # 温差 × 9 = 角度
                else:
                    speed = 0
                fan_speed_bar.set_width(speed)

                # 刷新图形
                fig.canvas.draw()
                fig.canvas.flush_events()

                # 终端输出
                status = "🔥 风扇运转" if current > target else "💤 待机"
                print(f"\r当前:{current:.1f}°C | 目标:{target:.1f}°C | {status}  ", end='')



except KeyboardInterrupt:
    print("\n\n系统关闭。")
    ser.close()