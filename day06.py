# ========== 常量与函数定义（放在最外层） ==========
STANDARD_MODULES = [0.5, 0.6, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]


def calculate_module(outer_diameter, tooth_count):
    """计算齿轮模数"""
    return outer_diameter / (tooth_count + 2)


def is_standard_module(module_value):
    """判断模数是否为标准值，返回 (是否标准, 标准值)"""
    rounded_value = round(module_value, 4)
    for std in STANDARD_MODULES:
        if rounded_value == std:
            return True, std
    return False, None


def find_nearest_standard(module_value):
    """找到最接近的标准模数"""
    nearest = STANDARD_MODULES[0]
    min_diff = abs(module_value - nearest)
    for std in STANDARD_MODULES:
        diff = abs(module_value - std)
        if diff < min_diff:
            min_diff = diff
            nearest = std
    return nearest


def get_float_input(prompt):
    """反复询问直到用户输入一个合法的浮点数"""
    while True:
        user_input = input(prompt)
        try:
            return float(user_input)
        except ValueError:
            print(f"输入有误'{user_input}'不是一个有效的数字，请重新输入。")


def get_int_input(prompt):
    """反复询问直到用户输入一个合法的整数"""
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)
        except ValueError:
            print(f"输入有误：'{user_input}' 不是一个有效的整数，请重新输入。")


# ========== 主程序 ==========
print("=" * 50)
print("             齿轮模数计算与选型工具")
print("=" * 50)

while True:
    # 获取输入（带防呆）
    outer_diameter = get_float_input("请输入齿轮外径（mm）：")
    tooth_count = get_int_input("请输入齿数：")

    # 计算
    m = calculate_module(outer_diameter, tooth_count)
    is_std, std_value = is_standard_module(m)

    # 输出结果
    print("\n" + "=" * 50)
    print("计算结果")
    print("-" * 50)
    print(f"外径：{outer_diameter} mm")
    print(f"齿数：{tooth_count}")
    print(f"计算模数：{m:.4f}")

    if is_std:
        print(f"✅ 该模数为标准模数（第一系列：{std_value}）")
    else:
        nearest = find_nearest_standard(m)
        print(f"⚠️ 该模数不是标准模数")
        print(f"建议选用最近的标准模数：{nearest}")
        new_diameter = nearest * (tooth_count + 2)
        print(f"调整建议：如果保持齿数不变，外径应调整为 {new_diameter:.2f} mm")

    print("=" * 50)

    # 退出判断
    order = input("按回车输入下一组数据，输入 q 并回车退出：")
    if order == "q" or order == "Q":
        print("程序结束，再见！")
        break