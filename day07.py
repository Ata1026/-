import numpy as np

torques = np.array([100, 200, 500, 1000])
diameters = np.array([20, 15, 25, 20])
tau_allow = 60

# 批量计算剪应力（抗扭截面系数 Wp = π·d³/16）
tau_actual = torques * 1000 / (np.pi * diameters**3 / 16)

print("轴强度校核结果")
print("=" * 50)
for idx, stress in enumerate(tau_actual, start=1):  # 直接从 1 开始编号
    sf = tau_allow / stress
    status = "合格" if sf >= 1 else "不合格"
    print(f"轴{idx}：剪应力 = {stress:.2f} MPa，安全系数 = {sf:.2f}，{status}")