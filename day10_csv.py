import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
data=np.loadtxt("C:/Users/M/Desktop/python_learning/motor_data.csv",delimiter=",",skiprows=1,encoding='utf-8')
time=data[:,0]
rpm=data[:,1]
temp=data[:,2]
print("="*50)
print("电机测试数据统计")
print("="*50)
print(f"数据点数：{len(time)}")
print(f"最高温度：{np.max(temp):.1f} ℃，发生在第 {time[np.argmax(temp)]:.1f} 秒")
print(f"最高转速：{np.max(rpm):.0f} RPM")
print(f"平均温度：{np.mean(temp):.1f} ℃")
print(f"温度标准差：{np.std(temp):.2f} ℃")
fig,axes=plt.subplots(2,1,figsize=(10,8),sharex=True)
ax1=axes[0]
ax1.plot(time,rpm,'b-',linewidth=2,label='转速')
ax1.set_ylabel("转速(RPM)")
ax1.set_title("电机运行数据分析")
ax1.legend(loc='best')
ax1.grid(True,alpha=0.3)
max_rpm=np.max(rpm)
max_rpm_time=time[np.argmax(rpm)]
ax1.plot(max_rpm_time,max_rpm,'ro',markersize=8)
ax1.annotate(f'最高转速{max_rpm:.0f}RPM',
             xy=(max_rpm_time,max_rpm),
             xytext=(max_rpm_time+0.5,max_rpm-500),
             arrowprops=dict(arrowstyle='->',color='red'),
             fontsize=10,color='red')
ax2=axes[1]
ax2.plot(time,temp,'r-',linewidth=2,label="温度")
ax2.fill_between(time,20,temp,color="red",alpha=0.1)
ax2.set_xlabel("时间(s)")
ax2.set_ylabel("温度(℃)")
ax2.legend(loc="best")
ax2.grid(True,alpha=0.3)
max_temp=np.max(temp)
max_temp_time=time[np.argmax(temp)]
ax2.plot(max_temp_time,max_temp,'bo',markersize=8)
ax2.annotate(f'最高温度{max_temp:.1f}℃',
             xy=(max_temp_time,max_temp),
             xytext=(max_temp_time+0.5,max_temp-2),
             arrowprops=dict(arrowstyle='->',color='blue'),
             fontsize=10,color='blue')
ax2.axhline(y=45,color='orange',linestyle='--',alpha=0.7,label='温度警戒线 45℃')
plt.tight_layout()
plt.show()