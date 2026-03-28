import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


V_measured = np.array([3.350, 0.000, 0.382, 0.716, 1.039, 1.397, 1.819, 2.255, 2.633,
                       2.875, 3.095, 3.154, 3.199, 3.233, 3.261, 3.283, 3.296, 3.314, 3.324, 3.332, 3.338, 3.352])
I_measured = np.array([0, 58.26, 58.87, 58.77, 58.87, 59.20, 59.23, 58.87, 54.52,
                       48.15, 36.40, 31.00, 26.04, 21.79, 17.66, 14.11, 11.91, 8.75, 6.90, 5.22, 4.03, 1.01])


sort_idx = np.argsort(V_measured)
V_measured = V_measured[sort_idx]
I_measured = I_measured[sort_idx]

f_interp = interp1d(V_measured, I_measured, kind='cubic', fill_value='extrapolate')

V_max_data = max(V_measured)
V_dense = np.linspace(0, V_max_data + 0.01, 500)
I_dense = f_interp(V_dense)

I_dense = np.maximum(I_dense, 0)

if V_measured[0] == 0:
    I_sc = I_measured[0]
else:
    I_sc = f_interp(0) if 0 >= V_measured[0] else I_measured[0]


idx_zeros = np.where(I_dense <= 0)[0]
if len(idx_zeros) > 0:
    idx = idx_zeros[0]
    if idx > 0:
        Voc = np.interp(0, I_dense[idx-1:idx+1][::-1], V_dense[idx-1:idx+1][::-1])
    else:
        Voc = V_dense[0]
else:
    Voc = V_dense[-1]

# 功率曲线
P_dense = V_dense * I_dense
# 最大功率点
max_power_idx = np.argmax(P_dense)
V_mp = V_dense[max_power_idx]
I_mp = I_dense[max_power_idx]
P_max = P_dense[max_power_idx]

# 填充因子
FF = P_max / (Voc * I_sc) if Voc * I_sc != 0 else 0

# 输出计算结果（个人选择）
'''
print(f"短路电流 Isc = {I_sc:.3f} A")
print(f"开路电压 Voc = {Voc:.3f} V")
print(f"最大功率点: Vmp = {V_mp:.3f} V, Imp = {I_mp:.3f} A, Pmax = {P_max:.3f} W")
print(f"填充因子 FF = {FF:.3f}")
'''

plt.figure(figsize=(10, 5))

# I-V 曲线
plt.subplot(1, 2, 1)
plt.plot(V_dense, I_dense, 'b-', linewidth=2, label='拟合曲线')
plt.scatter(V_measured, I_measured, color='red', s=50, zorder=5, label='实测数据点')
plt.scatter([0], [I_sc], color='green', marker='s', zorder=5, label=f'Isc = {I_sc:.2f} A')
plt.scatter([Voc], [0], color='orange', marker='s', zorder=5, label=f'Voc = {Voc:.2f} V')
plt.scatter([V_mp], [I_mp], color='purple', marker='*', s=120, zorder=5,
            label=f'最大功率点 ({V_mp:.2f} V, {I_mp:.2f} A)')
plt.xlabel('电压 (V)')
plt.ylabel('电流 (mA)')
plt.title('单个电池(90cm)的I-V曲线')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='best')
plt.xlim(0, V_max_data + 0.02)
plt.ylim(0, I_sc * 1.05)

# P-V 曲线
plt.subplot(1, 2, 2)
plt.plot(V_dense, P_dense, 'r-', linewidth=2, label='功率曲线')
plt.scatter([V_mp], [P_max], color='purple', marker='*', s=120, zorder=5,
            label=f'Pmax = {P_max:.2f} W')
plt.xlabel('电压 (V)')
plt.ylabel('功率 (mW)')
plt.title('单个电池(90cm)的P-V曲线')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='best')
plt.xlim(0, V_max_data + 0.02)
plt.ylim(0, P_max * 1.05)

plt.tight_layout()
plt.savefig('solar_cell_iv_from_measurement.png', dpi=150)
plt.show()

# data->
# 90cm
'''
V_measured = np.array([3.360, 0.000, 2.791, 2.528, 2.294, 2.003, 1.760, 1.614, 1.465,
                       1.210, 3.357, 1.048, 0.788, 0.358, 3.131, 3.222, 3.274, 3.295, 3.309, 3.323, 3.335, 3.346])  # 示例电压
I_measured = np.array([0, 34.28, 33.29, 33.80, 33.74, 33.78, 33.95, 34.04, 34.13,
                       34.12, 3.77, 34.18, 34.24, 34.28, 26.10, 19.89, 14.81, 12.28, 10.45, 8.61, 6.93, 5.40])
'''

# 75cm
'''
V_measured = np.array([3.417, 0.000, 0.849, 1.307, 1.531, 1.865, 2.323, 2.753, 2.993,
                       0.549, 3.383, 0.320, 1.149, 2.010, 2.534, 3.096, 3.185, 3.219, 3.277, 3.316, 3.345, 3.365, 3.376])  
I_measured = np.array([0, 45.02, 44.98, 44.87, 44.80, 44.72, 44.56, 44.19, 42.03,
                       45.03, 3.79, 45.16, 45.04, 44.97, 44.76, 38.65, 32.80, 29.09, 22.17, 16.69, 11.54, 7.70, 5.35])
'''
# 60cm
'''
V_measured = np.array([3.39, 0.00, 0.12, 0.57, 1.04, 1.43, 1.67, 2.23, 3.02,
                       3.21, 3.27, 3.31, 3.33, 3.35, 3.36, 3.37, 3.38, 1.76, 1.95, 2.16, 2.39, 2.82])  
I_measured = np.array([0, 41.52, 42.02, 41.92, 41.77, 41.48, 41.37, 41.18, 39.33,
                       29.90, 22.20, 17.16, 13.46, 9.38, 7.55, 5.88, 3.42, 41.18, 41.22, 40.95, 40.86, 40.65])
'''
# 两电池并联
'''
V_measured = np.array([3.350, 0.000, 0.382, 0.716, 1.039, 1.397, 1.819, 2.255, 2.633,
                       2.875, 3.095, 3.154, 3.199, 3.233, 3.261, 3.283, 3.296, 3.314, 3.324, 3.332, 3.338, 3.352])  
I_measured = np.array([0, 58.26, 58.87, 58.77, 58.87, 59.20, 59.23, 58.87, 54.52,
                       48.15, 36.40, 31.00, 26.04, 21.79, 17.66, 14.11, 11.91, 8.75, 6.90, 5.22, 4.03, 1.01])
'''
# 两电池串联
'''
V_measured = np.array([6.66, 0, 0.57, 0.94, 1.57, 1.73, 1.95, 2.22, 2.46,
                       2.66, 2.88, 3.16, 3.37, 3.47, 3.72, 4.10, 4.44, 4.88, 5.53, 5.93, 6.13, 6.28, 6.38, 6.44, 6.50, 6.56, 6.60, 6.69])  
I_measured = np.array([0, 33.91, 33.74, 33.72, 33.60, 33.85, 33.68, 33.67, 33.52,
                       33.36, 33.39, 33.18, 33.11, 32.98, 32.88, 32.79, 32.66, 32.69, 32.34, 30.27, 27.34, 23.46, 19.62, 16.85, 13.80, 10.68, 7.84, 6.61])
'''

# 两电池并联
'''
V_measured = np.array([3.350, 0.000, 0.382, 0.716, 1.039, 1.397, 1.819, 2.255, 2.633,
                       2.875, 3.095, 3.154, 3.199, 3.233, 3.261, 3.283, 3.296, 3.314, 3.324, 3.332, 3.338, 3.352])  # 示例电压
I_measured = np.array([0, 58.26, 58.87, 58.77, 58.87, 59.20, 59.23, 58.87, 54.52,
                       48.15, 36.40, 31.00, 26.04, 21.79, 17.66, 14.11, 11.91, 8.75, 6.90, 5.22, 4.03, 1.01])
'''

# 两串两并
'''
V_measured = np.array([10.03, 0.00, 0.67, 1.35, 1.87, 2.31, 2.75, 3.28, 3.75,
                       4.11, 4.55, 5.26, 6.00, 6.64, 7.59, 8.06, 8.42, 8.99, 9.34, 9.52, 9.66, 9.74, 9.80, 9.97])  # 示例电压
I_measured = np.array([0, 23.81, 23.48, 23.04, 22.87, 22.78, 22.54, 22.50, 22.43,
                       22.30, 22.18, 22.05, 21.92, 21.80, 21.75, 21.63, 21.68, 21.53, 20.18, 17.84, 14.41, 11.90, 9.90, 2.78])
'''
# 一串三并
'''
V_measured = np.array([6.62, 0.000, 0.10, 0.55, 1.00, 1.48, 1.92, 2.46, 2.99,
                       3.32, 3.83, 4.27, 4.81, 5.28, 5.71, 6.12, 6.27, 6.34, 6.42, 6.48, 6.52, 6.57])  # 示例电压
I_measured = np.array([0, 32.44, 32.76, 32.48, 32.47, 42.48, 32.07, 31.44, 31.09,
                       30.85, 30.34, 30.17, 29.88, 29.68, 29.28, 23.83, 19.33, 16.05, 12.33, 9.10, 6.59, 2.52])
'''