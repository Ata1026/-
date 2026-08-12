import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def forward_kinematics(theta1, theta2, L1=1.5, L2=0.5):
    x_elbow = L1 * np.cos(theta1)
    y_elbow = L1 * np.sin(theta1)
    x_end = x_elbow + L2 * np.cos(theta1 + theta2)
    y_end = y_elbow + L2 * np.sin(theta1 + theta2)
    return x_elbow, y_elbow, x_end, y_end

# ---------- 参数 ----------
theta1 = np.radians(45)                     # 关节1固定45°
theta2_array = np.linspace(0, 2*np.pi, 200) # 关节2转一圈

# ---------- 画出末端轨迹（灰色虚线圆） ----------
_, _, x_traj, y_traj = forward_kinematics(theta1, theta2_array)
plt.plot(x_traj, y_traj, '-g', alpha=0.7, label='末端轨迹')

# ---------- 挑6个角度，画出机械臂姿态 ----------
for theta2_sample in np.radians([0, 60, 120, 180, 240, 300]):
    x_elbow, y_elbow, x_end, y_end = forward_kinematics(theta1, theta2_sample)
    # 连杆1（蓝色），连杆2（红色），肘关节（黑色方块），末端（绿色圆）
    plt.plot([0, x_elbow], [0, y_elbow], 'b-', linewidth=2)
    plt.plot([x_elbow, x_end], [y_elbow, y_end], 'r-', linewidth=2)
    plt.plot(x_elbow, y_elbow, 'ks', markersize=6)
    plt.plot(x_end, y_end, 'go', markersize=8)

# 机械臂的基座
plt.plot(0, 0, 'ok', markersize=10)

# ---------- 图片美化 ----------
plt.axhline(0, color='gray', linestyle=':', alpha=0.3)
plt.axvline(0, color='gray', linestyle=':', alpha=0.3)
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title("二连杆机械臂：固定 θ₁=45°，θ₂ 转动一圈")
plt.grid(True, alpha=0.3)
plt.gca().set_aspect('equal')
plt.xlim(-2.5, 2.5)
plt.ylim(-2.5, 2.5)
plt.show()