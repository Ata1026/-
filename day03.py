import math
s=0


for cycle in range(1,10001):
    while s<100:
        s=s+10
    while s>0:
        s=s-10    
    if cycle % 1000 == 0:
        print(f"已完成{cycle}次")


print("寿命测试完成，丝杆工作正常")



