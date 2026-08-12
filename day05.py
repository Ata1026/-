inventory = [
    {"name": "内轮", "stock": 70, "min_stock": 10},
    {"name": "外轮", "stock": 60, "min_stock": 10},
    {"name": "前轮", "stock": 84, "min_stock": 10},
    {"name": "后轮", "stock": 7,  "min_stock": 10},
    {"name": "车轮", "stock": 9,  "min_stock": 10},
]


def check_inventory(part):
    """判断单个零件是否需要补货，返回状态字符串"""
    if part["stock"] < part["min_stock"]:
        return "需要补货"
    else:
        return "库存充足"


# 打印表头
print("当前所有零件的库存状态")
print("=" * 60)
print(f"{'零件名称':<8} {'库存数量':<10} {'安全库存':<10} {'状态':<10}")
print("-" * 60)

# 一个循环完成所有事情：打印表格行 + 判断补货状态
for part in inventory:
    name = part["name"]
    stock = part["stock"]
    min_stock = part["min_stock"]
    status = check_inventory(part)          # 直接传整个字典
    print(f"{name:<8} {stock:<10} {min_stock:<10} {status:<10}")

print("=" * 60)