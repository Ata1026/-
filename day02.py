P=1.6
D=1000
sigma=160
delta_c=2
delta=P*D/(2*sigma-P)+delta_c
delta_actual=10
if delta_actual>=delta:
    print("校核通过，壁厚足够")

elif delta_actual>0.8*delta:
    print("警告：安全裕度不足，请复核")
else:
    print("壁厚严重不足，禁止使用！")    
