import numpy as np

stress = np.array([353.7, 198.9, 127.3, 88.4, 49.7])
allowable = 160

# 比较运算 → 布尔数组
pass_idx = stress <= allowable
print(pass_idx)