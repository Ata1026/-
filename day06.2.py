import math


def get_float_input(prompt):
    """防呆：反复询问直到用户输入合法的浮点数"""
    while True:
        user_input = input(prompt)
        try:
            return float(user_input)
        except ValueError:
            print(f"输入有误：'{user_input}' 不是有效数字，请重新输入。")


def get_int_input(prompt):
    """防呆：反复询问直到用户输入合法的整数"""
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)
        except ValueError:
            print(f"输入有误：'{user_input}' 不是有效整数，请重新输入。")


# ========== 三个计算函数 ==========
# 你来补充：gear_module_calc()
def gear_module_calc(D,z):
    m=D/(z+2)
    return m
    # 你来补充：bolt_area_calc()
def bolt_area_calc(d):
    A=math.pi*d**2/4
    return A
# 你来补充：wall_thickness_calc()
def wall_thickness_calc(P,D,q,C=2):
    thick=P*D/(2*q-P)+C
    return thick

# ========== 主菜单 ==========
while True:
    print("\n" + "=" * 50)
    print("      机械设计计算工具箱")
    print("=" * 50)
    print("1. 齿轮模数计算")
    print("2. 螺栓截面积计算")
    print("3. 压力容器壁厚计算")
    print("0. 退出")
    print("=" * 50)

    choice = input("请选择功能（0-3）：")

    if choice == "0":
        print("程序结束，再见！")
        break
    elif choice == "1":
        D=get_float_input("请输入齿轮外径（mm）：")
        z=get_int_input("请输入齿数：")
        m=gear_module_calc(D,z)
        print(f"齿轮模数为{m}")
        # 齿轮模数计算（你来实现）
        pass
    elif choice == "2":
        d=get_float_input("请输入螺栓直径")
        A=bolt_area_calc(d)
        print(f"螺栓截面积为{A}")
        # 螺栓截面积计算（你来实现）
        pass
    elif choice == "3":
        P=get_float_input("请输入设计压力")
        D=get_float_input("请输入筒体内径")
        q=get_float_input("请输入许用内力")
        thick=wall_thickness_calc(P,D,q)
        print(f"压力容器壁厚为{round(thick,4)}")

        # 压力容器壁厚计算（你来实现）
        pass
    else:
        print("输入无效，请输入 0、1、2 或 3。")