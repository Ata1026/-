# ==================== 1. 导入库 ====================
import serial                     # 用于和 Arduino 通过 USB 串口通信
import time                       # 用于延时等待
from collections import deque     # 用于创建固定长度的历史数据队列
import matplotlib.pyplot as plt   # 用于画实时动态图表

# ==================== 2. 连接 Arduino ====================
PORT = 'COM4'                     # Arduino 在你电脑上的串口号（在 Arduino IDE 工具→端口里查看）
BAUD = 9600                       # 波特率，必须和 Arduino 程序里的 Serial.begin(9600) 一致

ser = serial.Serial(PORT, BAUD, timeout=1)  # 创建串口对象，timeout=1 表示 1 秒没收到数据就放弃
time.sleep(2)                     # 等待 Arduino 上电复位完成（刚接 USB 时 Arduino 会自动重启一次）
print(f"✅ 已连接 Arduino（{PORT}）")
print("倒车雷达系统启动\n")

# ==================== 3. 创建数据存储队列 ====================
history_len = 50                  # 最多保留 50 个历史数据点
# 下面两个都是双端队列，每个最多装 50 个数据，满了自动把最旧的挤出去
time_axis = deque([0] * history_len, maxlen=history_len)           # 时间轴，初始化为 50 个 0
distance_history = deque([0] * history_len, maxlen=history_len)   # 距离历史，初始化为 50 个 0
time_counter = 0                  # 时间计数器，每收到一次有效数据就 +1

# ==================== 4. 设置实时绘图窗口 ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']  # 解决中文显示乱码
plt.rcParams['axes.unicode_minus'] = False                       # 解决负号显示问题
plt.ion()                           # 开启交互模式，允许后面动态更新图表
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # 创建上下两个子图，整张画布 10×8 英寸

# ---- 子图 1：距离实时曲线 ----
line_dist, = ax1.plot([], [], 'b-', linewidth=2, label='当前距离')  # 画一条蓝色空线，后面会动态填数据
ax1.set_ylim(0, 100)               # Y 轴范围固定在 0~100 cm
ax1.set_xlim(-50, 0)               # X 轴初始范围
ax1.set_ylabel("距离 (cm)")         # Y 轴标签
ax1.set_title("倒车雷达 - 实时距离监控")  # 子图 1 标题
ax1.legend(loc='upper left')        # 显示图例，放在左上角
ax1.grid(True, alpha=0.3)           # 显示半透明网格线

# ---- 子图 2：当前距离水平进度条 ----
# 画一个初始长度为 0 的绿色水平柱状图
bar_distance = ax2.barh(['距离'], [0], color='green', height=0.5)[0]
# ↑ barh 返回一个列表，[0] 取出列表里唯一的那个矩形条对象
ax2.set_xlim(0, 100)                # X 轴范围 0~100 cm
ax2.set_xlabel("距离 (cm)")          # X 轴标签
ax2.set_title("当前距离指示")         # 子图 2 标题

plt.tight_layout()                  # 自动调整子图间距，防止文字重叠
plt.show()                          # 弹出图形窗口

# ==================== 5. 主循环：不断读取串口数据并刷新图表 ====================
try:
    while True:                           # 无限循环，直到用户按下 Ctrl+C
        if ser.in_waiting > 0:            # 如果串口接收缓冲区里有数据（Arduino 发东西来了）
            line = ser.readline()         # 读取一行原始字节，格式类似 b'35.2,30\r\n'
            data_str = line.decode('utf-8').strip()  # 字节→字符串，剥掉末尾的 \r 和 \n
            if ',' in data_str:           # 确认数据里有逗号（防止读到空行或乱码）
                parts = data_str.split(',')  # 按逗号切开成两段
                try:
                    distance = float(parts[0])   # 第一段：当前距离（转成小数）
                    threshold = int(parts[1])    # 第二段：报警阈值（转成整数）
                except ValueError:
                    continue              # 如果转数字失败（收到乱码），跳过这次

                # ---- 把新数据加入历史队列 ----
                time_counter += 1                      # 时间 +1
                time_axis.append(time_counter)         # 新时间戳加入时间轴
                distance_history.append(distance)      # 新距离值加入历史队列

                # ---- 更新距离曲线 ----
                line_dist.set_data(list(time_axis), list(distance_history))  # 更新曲线数据
                ax1.set_xlim(time_counter - 50, time_counter)  # X 轴自动跟随最新数据

                # ---- 更新距离进度条 ----
                bar_distance.set_width(distance)  # 设置进度条的宽度为当前距离值

                # 根据距离和阈值的关系，改变进度条颜色
                if distance <= threshold:
                    bar_distance.set_color('red')      # 危险 → 红色
                    status = "🔴 危险"
                elif distance <= threshold * 2:
                    bar_distance.set_color('orange')   # 警戒 → 橙色
                    status = "🟠 警戒"
                else:
                    bar_distance.set_color('green')    # 安全 → 绿色
                    status = "🟢 安全"

                # ---- 刷新图形界面 ----
                fig.canvas.draw()          # 强制重绘画布
                fig.canvas.flush_events()  # 处理窗口事件，防止窗口卡死

                # ---- 终端输出（和昨天一样的原地刷新效果） ----
                print(f"\r距离:{distance:6.1f}cm | 阈值:{threshold}cm | {status}  ", end='')
                # \r 让光标回到行首，end='' 阻止换行，实现同一行动态刷新

        time.sleep(0.05)   # 稍微等待 0.05 秒，防止循环跑太快消耗 CPU

except KeyboardInterrupt:   # 用户按下 Ctrl+C 时触发
    print("\n\n系统关闭。")  # \n\n 换两行，避免和进度条挤在一起
    ser.close()             # 关闭串口连接，释放 COM 口