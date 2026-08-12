import pyfirmata2
import time

PORT = 'COM4'                     # 改成你的实际端口
board = pyfirmata2.Arduino(PORT)
time.sleep(2)                     # 等板子复位
print("✅ Arduino 已连接！")
led_pin=9
board.digital[led_pin].mode = pyfirmata2.OUTPUT

# 使用 get_pin 获取 PWM 引脚
led1 = board.get_pin('d:9:p')  
led2=board.get_pin('d:3:p')   # 数字口9，PWM 模式

print("开始呼吸灯效果，按 Ctrl+C 停止...")

try:
    while True:
        # 渐亮
        for i in range(20, 81, 1):
            led1.write(i / 100.0)
            led2.write((100-i)/100)  # 0.0 → 1.0
            time.sleep(0.02)
        # 渐暗
        for i in range(20, 81, 1):
            led1.write((100-i) / 100.0)
            led2.write(i/100)
            time.sleep(0.02)
except KeyboardInterrupt:
    led1.write(0)
    led2.write(0)
    print("\n呼吸灯已停止。")
    board.exit()