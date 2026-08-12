import pyfirmata2
import time

PORT = 'COM4'          # 请改成你自己的端口
board = pyfirmata2.Arduino(PORT)

        # 关键：等板子复位结束，忽略启动时的闪烁
print("✅ 成功连接 Arduino！")

led_pin1 = 13
led_pin2=12
board.digital[led_pin1].mode = pyfirmata2.OUTPUT
board.digital[led_pin2].mode = pyfirmata2.OUTPUT


while True:
    b=input("请输入数字")
    try: a=float(b)
    except ValueError:
           break

    if a>5:
            board.digital[13].write(1)
            time.sleep(0.1)
            board.digital[13].write(0)
            time.sleep(0.1)
    elif a<5:
            board.digital[12].write(1)
            time.sleep(0.1)
            board.digital[12].write(0)
            time.sleep(0.1)
    else:
            board.digital[13].write(1)
            time.sleep(0.1)
            board.digital[12].write(1)
            time.sleep(0.1)
            board.digital[13].write(0)
            time.sleep(0.1)
            board.digital[12].write(0)
            time.sleep(0.1)
    time.sleep(1)
         







