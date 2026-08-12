import pyfirmata2
import time

board = pyfirmata2.Arduino('COM4')  # 替换为你的端口
print("连接成功")
led = board.get_pin('d:13:o')  # d=digital, 13=pin, o=output

for _ in range(5):
    led.write(1)
    time.sleep(0.5)
    led.write(0)
    time.sleep(0.5)

board.exit()
