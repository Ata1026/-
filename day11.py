import numpy as np
import os
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
t=np.linspace(0,2,1000)
freq=0.5
zeta=0.15
amplitude=10*np.exp(-zeta*2*np.pi*freq*t)
displacement=amplitude*np.sin(2*np.pi*freq*t)
noise=np.random.normal(0,0.2,size=len(t))
displacement_nosiy=displacement+noise
header="时间(s),位移(mm)"
np.savetxt("vibration_data.csv",
           np.column_stack((t,displacement_nosiy)),
           delimiter=",",header=header,comments='',fmt='%.6f')
print("✅ 振动数据已保存为 vibration_data.csv")
print(f"文件保存在：{os.path.abspath('vibration_data.csv')}")
data=np.loadtxt("vibration_data.csv",delimiter=',',skiprows=1)
t_read=data[:,0]
disp_read=data[:,1]
print("="*50)
print("振动数据分析报告")
print("=" * 50)
print(f'采集点数:{len(t_read)}')
print(f'采样时长:{t_read[-1]-t_read[0]:.2f}秒')
print(f'最大位移:{np.max(disp_read):.3f}mm')
print(f'最小位移:{np.min(disp_read):.3f}mm')
print(f"振动幅度范围:{np.ptp(disp_read):.3f}mm")
sampling_rate=500
n=len(t_read)
fft_result=np.fft.fft(disp_read)
freqs=np.fft.fftfreq(n,d=1/sampling_rate)
positive_freqs=freqs[:n//2]
fft_magnitude=np.abs(fft_result[:n//2])/n*2
top_idx=np.argmax(fft_magnitude)
dominant_freq=positive_freqs[top_idx]
print(f"主要振动频率:{dominant_freq:.1f}Hz")
# ========== 5. 找振动峰值 ==========
def find_peaks(signal, min_distance=10):
    """
    简单的峰值检测函数
    min_distance: 两个峰值之间至少间隔多少个采样点
    """
    peaks = []
    for i in range(min_distance, len(signal) - min_distance):
        # 判断当前点是否大于左右相邻点
        if signal[i] > signal[i-1] and signal[i] > signal[i+1]:
            # 判断是否是局部区域内最大的
            local_start = max(0, i - min_distance)
            local_end = min(len(signal), i + min_distance)
            if signal[i] == np.max(signal[local_start:local_end]):
                peaks.append(i)
    return np.array(peaks)

peak_indices = find_peaks(disp_read)
# 按幅值排序，取前 5 个最大峰值
top_5_peaks = peak_indices[np.argsort(np.abs(disp_read[peak_indices]))[-5:]]
top_5_peaks = np.sort(top_5_peaks)  # 按时间排序

print(f"检测到 {len(peak_indices)} 个波峰，前 5 个最大峰值：")
for i, idx in enumerate(top_5_peaks):
    print(f"  峰值{i+1}：时间 {t_read[idx]:.3f}s，位移 {disp_read[idx]:.3f} mm")
fig,axes=plt.subplots(3,1,figsize=(12,10))
ax1=axes[0]
ax1.plot(t_read,disp_read,'b-',linewidth=0.8,label='振动信号')
ax1.scatter(t_read[top_5_peaks],disp_read[top_5_peaks],
            color='red',s=60,label='前5大峰值')
ax1.set_ylabel("位移(Hz)")
ax1.set_title("幅值(mm)")
ax1.legend(loc='best')
ax1.grid(True,alpha=0.3)
ax2=axes[1]
ax2.stem(positive_freqs[:100],fft_magnitude[:100],linefmt='g-',markerfmt='go',basefmt='')
ax2.set_xlabel("频率 (Hz)")
ax2.set_ylabel("幅值 (mm)")
ax2.set_title(f"频谱分析（主要频率：{dominant_freq:.1f} Hz）")
ax2.grid(True, alpha=0.3)    
ax3=axes[2]
peak_labels=[f'{t_read[idx]:.2f}s'for idx in top_5_peaks]
peak_values=np.abs(disp_read[top_5_peaks])
colors = ['#FF6B6B', '#FFA07A', '#FFD700', '#90EE90', '#87CEEB']
ax3.bar(peak_labels, peak_values, color=colors, edgecolor='black')
ax3.set_xlabel("峰值时刻")
ax3.set_ylabel("位移幅值 (mm)")
ax3.set_title("振动峰值统计（前 5 大）")
ax3.grid(True, alpha=0.3, axis='y')
for i ,(label,val) in enumerate(zip(peak_labels,peak_values)):
    ax3.text(i,val+0.1,f'{val:.2f}',ha='center',fontsize=10)
plt.tight_layout()
plt.show()    