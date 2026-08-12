import math
# ↑ 导入数学库，我们需要用到里面的 pi（圆周率）

# ========== 函数1：计算轴强度 ==========
def shaft_strength(torque, diameter):
    # ↑ def 是定义函数的关键字
    # ↑ shaft_strength 是函数名，我们自己起的
    # ↑ (torque, diameter) 是参数，调用时传进来
    # ↑ 冒号表示函数体开始

    """
    计算实心圆轴的剪应力
    参数：扭矩 torque (N·m), 轴直径 diameter (mm)
    返回：剪应力 (MPa)
    """
    # ↑ 三引号包起来的是文档字符串，写给人看的说明，程序会跳过

    r = diameter / 2
    # ↑ 计算半径，直径除以2。单位是 mm

    Wp = math.pi * r**3 / 2
    # ↑ 抗扭截面系数公式：Wp = π * r³ / 2
    # ↑ math.pi 就是 π（约 3.14159）
    # ↑ r**3 表示 r 的三次方
    # ↑ 单位是 mm³

    shear_stress = torque * 1000 / Wp
    # ↑ 剪应力 = 扭矩 / 抗扭截面系数
    # ↑ torque * 1000 是把 N·m 转成 N·mm（1 N·m = 1000 N·mm）
    # ↑ 这样分子分母单位统一，结果单位是 MPa

    return shear_stress
    # ↑ 把计算结果送回给调用者


# ========== 函数2：判断是否安全 ==========
def check_safety(actual_stress, allowable_stress):
    # ↑ 定义第二个函数，两个参数：实际应力、许用应力

    """返回安全系数和是否合格"""

    factor = allowable_stress / actual_stress
    # ↑ 安全系数 = 许用应力 / 实际应力
    # ↑ 如果 factor >= 1，说明许用的大于实际的，安全

    if factor >= 1.0:
        return factor, "合格"
        # ↑ 返回两个值：安全系数 和 文字判断结果
    else:
        return factor, "不合格"
        # ↑ 同样返回两个值


# ========== 主程序 ==========
tau_allow = 60
# ↑ 设定许用剪应力为 60 MPa，你可以改这个值看结果变化

test_cases = [
    (100, 20),
    (200, 15),
    (500, 25),
    (1000, 20),
]
# ↑ 一个列表，里面每个括号是一组测试数据：(扭矩, 轴径)
# ↑ 第一组：扭矩 100 N·m，轴径 20 mm
# ↑ 第二组：扭矩 200 N·m，轴径 15 mm
# ↑ 以此类推

print("轴强度校核报告")
print("=" * 40)
# ↑ "=" * 40 表示把 "=" 这个字符重复 40 次，画一条分隔线

for torque, dia in test_cases:
    # ↑ for 循环遍历 test_cases 列表
    # ↑ 每次取出一个元组，自动拆开
    # ↑ torque 拿到第一个值（扭矩），dia 拿到第二个值（轴径）

    tau = shaft_strength(torque, dia)
    # ↑ 调用函数1，把扭矩和轴径传进去
    # ↑ 函数返回的剪应力存到变量 tau 里

    factor, b = check_safety(tau, tau_allow)
    # ↑ 调用函数2，把实际应力和许用应力传进去
    # ↑ 函数返回两个值，factor 接收安全系数，status 接收"合格"/"不合格"

    print(f"扭矩{torque:4d} N·m，轴径{dia:2d} mm → 应力{tau:6.2f} MPa，安全系数{factor:.2f}，{b}")
    # ↑ f"..." 是格式化字符串
    # ↑ {torque:4d}  —— 整数，占 4 个字符宽度，右对齐
    # ↑ {dia:2d}     —— 整数，占 2 个字符宽度
    # ↑ {tau:6.2f}   —— 浮点数，占 6 个字符宽度，保留 2 位小数
    # ↑ {factor:.2f} —— 浮点数，保留 2 位小数
    # ↑ {status}     —— 字符串，直接放进去