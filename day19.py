import serial
import matplotlib.pyplot as plt
from collections import deque
import time
import csv

# ==================== 连接 Arduino ====================
PORT = 'COM4'          # 改成你的实际端口
BAUD = 115200          # 必须和 Arduino 程序一致

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print(f"✅ 已连接 Arduino（{PORT}）")
print("多功能环境监控终端 - 系统启动\n")

# ==================== 数据存储队列（最近 100 个点） ====================
history_len = 100
time_axis = deque([0]*history_len, maxlen=history_len)
temp_history = deque([0]*history_len, maxlen=history_len)
humi_history = deque([0]*history_len, maxlen=history_len)
light_history = deque([0]*history_len, maxlen=history_len)
vib_history = deque([0]*history_len, maxlen=history_len)
time_counter = 0

# ==================== 设置实时绘图（四张子图） ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.ion()
fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

# 子图1：温度（红色）
line_temp, = axes[0].plot([], [], 'r-', linewidth=1.5, label='温度 (°C)')
axes[0].set_ylim(0, 50)
axes[0].set_ylabel("°C")
axes[0].set_title("环境温度")
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)
axes[0].axhline(y=35, color='orange', linestyle='--', alpha=0.7, label='高温阈值')

# 子图2：湿度（蓝色）
line_humi, = axes[1].plot([], [], 'b-', linewidth=1.5, label='湿度 (%)')
axes[1].set_ylim(0, 100)
axes[1].set_ylabel("%")
axes[1].set_title("环境湿度")
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='低湿阈值')

# 子图3：光线（绿色）
line_light, = axes[2].plot([], [], 'g-', linewidth=1.5, label='光线值')
axes[2].set_ylim(0, 1024)
axes[2].set_ylabel("ADC")
axes[2].set_title("环境亮度")
axes[2].legend(loc='upper left')
axes[2].grid(True, alpha=0.3)
axes[2].axhline(y=300, color='orange', linestyle='--', alpha=0.7, label='过暗阈值')

# 子图4：振动强度（紫色）
line_vib, = axes[3].plot([], [], 'm-', linewidth=1.5, label='振动强度')
axes[3].set_ylim(0, 1024)
axes[3].set_ylabel("ADC")
axes[3].set_xlabel("时间 (采样点)")
axes[3].set_title("振动强度")
axes[3].legend(loc='upper left')
axes[3].grid(True, alpha=0.3)
axes[3].axhline(y=500, color='red', linestyle='--', alpha=0.7, label='强振阈值')

plt.tight_layout()
plt.show()

# ==================== 创建 CSV 数据记录文件 ====================
csv_filename = f"env_full_{time.strftime('%Y%m%d_%H%M%S')}.csv"
csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['采样点', '温度(°C)', '湿度(%)', '光线值', '振动强度'])
print(f"📁 数据记录文件已创建：{csv_filename}\n")

# ==================== 主循环 ====================
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if ',' in line:
                parts = line.split(',')
                try:
                    temp = float(parts[0])
                    humi = float(parts[1])
                    light = int(parts[2])
                    vib = int(parts[3])
                except (ValueError, IndexError):
                    continue

                # 更新数据队列
                time_counter += 1
                time_axis.append(time_counter)
                temp_history.append(temp)
                humi_history.append(humi)
                light_history.append(light)
                vib_history.append(vib)

                # 更新四张曲线图
                line_temp.set_data(list(time_axis), list(temp_history))
                line_humi.set_data(list(time_axis), list(humi_history))
                line_light.set_data(list(time_axis), list(light_history))
                line_vib.set_data(list(time_axis), list(vib_history))

                # X 轴范围自动跟随最新数据
                axes[3].set_xlim(time_counter - history_len, time_counter)

                # 刷新画面
                fig.canvas.draw()
                fig.canvas.flush_events()

                # 终端实时输出（四列状态）
                temp_status = "🔥" if temp > 35 else "正常"
                humi_status = "💧" if humi < 20 else "正常"
                light_status = "🌙" if light < 300 else "☀️"
                vib_status = "⚠️" if vib > 500 else "正常"
                print(f"\r温度:{temp:.1f}°C({temp_status}) | "
                      f"湿度:{humi:.1f}%({humi_status}) | "
                      f"光线:{light:4d}({light_status}) | "
                      f"振动:{vib:4d}({vib_status})  ", end='')

                # 写入 CSV 文件
                csv_writer.writerow([time_counter, temp, humi, light, vib])
                csv_file.flush()  # 立即写入硬盘

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\n系统关闭。")

    # 关闭 CSV 文件
    csv_file.close()
    print(f"📁 数据已保存至：{csv_filename}")

    # 画一张最终的历史记录大图
    fig_final, ax_final = plt.subplots(4, 1, figsize=(14, 12))
    ax_final[0].plot(list(time_axis), list(temp_history), 'r-')
    ax_final[0].set_ylabel("温度 (°C)")
    ax_final[0].set_title("温度历史记录")
    ax_final[0].grid(True)

    ax_final[1].plot(list(time_axis), list(humi_history), 'b-')
    ax_final[1].set_ylabel("湿度 (%)")
    ax_final[1].set_title("湿度历史记录")
    ax_final[1].grid(True)

    ax_final[2].plot(list(time_axis), list(light_history), 'g-')
    ax_final[2].set_ylabel("光线值")
    ax_final[2].set_title("亮度历史记录")
    ax_final[2].grid(True)

    ax_final[3].plot(list(time_axis), list(vib_history), 'm-')
    ax_final[3].set_ylabel("振动强度")
    ax_final[3].set_xlabel("采样点")
    ax_final[3].set_title("振动历史记录")
    ax_final[3].grid(True)

    plt.tight_layout()
    plt.show()

    ser.close()
    print("程序结束。")