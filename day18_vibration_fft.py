import serial
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time

# ==================== 1. 连接 Arduino ====================
PORT = 'COM4'
BAUD = 115200  # 必须和 Arduino 程序里的 Serial.begin(115200) 一致

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print(f"✅ 已连接 Arduino（{PORT}）")
print("数字振动计 - FFT 频谱分析系统")
print("=" * 50)
print("敲击倾斜开关，观察振动波形和频谱图")
print("按 Ctrl+C 退出")
print("=" * 50 + "\n")

# ==================== 2. 设置绘图窗口 ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# 子图1：振动波形（时域）
line_wave, = ax1.plot([], [], 'b-', linewidth=1, label='振动信号')
ax1.set_xlim(0, 200)
ax1.set_ylim(-0.5, 1.5)
ax1.set_xlabel("采样点")
ax1.set_ylabel("信号值")
ax1.set_title("振动波形（时域）")
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

# 子图2：频谱图（频域）
ax2.set_xlim(0, 2500)  # 频率范围 0~2500 Hz（采样率 5000Hz 的一半）
ax2.set_ylim(0, 100)
ax2.set_xlabel("频率 (Hz)")
ax2.set_ylabel("幅值")
ax2.set_title("频谱分析（FFT）")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ==================== 3. 数据存储队列 ====================
history_len = 5  # 保留最近 5 次敲击的峰值频率
peak_freq_history = deque([0]*history_len, maxlen=history_len)

# ==================== 4. 主循环 ====================
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()

            if ',' in line:
                parts = line.split(',')
                if len(parts) == 200:
                    # 解析 200 个采样点
                    signal = np.array([int(x) for x in parts])

                    # ---- 绘制波形 ----
                    line_wave.set_data(range(200), signal)
                    ax1.set_xlim(0, 199)

                    # ---- FFT 频谱分析 ----
                    sampling_rate = 5000  # 采样率 5000 Hz（Arduino 端每 200μs 采一个点）
                    n = len(signal)
                    fft_result = np.fft.fft(signal)
                    freqs = np.fft.fftfreq(n, d=1/sampling_rate)

                    # 只取正频率部分
                    positive_freqs = freqs[:n//2]
                    fft_magnitude = np.abs(fft_result[:n//2]) / n * 2

                    # 找出前三个最高的频率峰值
                    sorted_indices = np.argsort(fft_magnitude)[::-1]  # 从大到小排序
                    top_3_freqs = positive_freqs[sorted_indices[:3]]
                    top_3_mags = fft_magnitude[sorted_indices[:3]]

                    # 输出峰值频率
                    dominant_freq = top_3_freqs[0]
                    peak_freq_history.append(dominant_freq)
                    print(f"\r固有频率: {dominant_freq:6.1f} Hz | 历史峰值: {list(peak_freq_history)}", end='')

                    # ---- 绘制频谱图 ----
                    ax2.clear()
                    ax2.plot(positive_freqs, fft_magnitude, 'g-', linewidth=1)
                    ax2.set_xlim(0, 2500)
                    ax2.set_ylim(0, max(fft_magnitude) * 1.2)
                    ax2.set_xlabel("频率 (Hz)")
                    ax2.set_ylabel("幅值")
                    ax2.set_title(f"频谱分析（主要频率: {dominant_freq:.1f} Hz）")
                    ax2.grid(True, alpha=0.3)

                    # 标记前三个峰值
                    for freq, mag in zip(top_3_freqs, top_3_mags):
                        ax2.plot(freq, mag, 'ro', markersize=6)
                        ax2.annotate(f'{freq:.0f}Hz',
                                     xy=(freq, mag),
                                     xytext=(freq+50, mag+5),
                                     fontsize=9, color='red')

                    # ---- 刷新图形 ----
                    fig.canvas.draw()
                    fig.canvas.flush_events()

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\n\n系统关闭。")
    ser.close()