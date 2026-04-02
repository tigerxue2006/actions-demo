import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # macOS
plt.rcParams['axes.unicode_minus'] = False

datasets = [
    # 90 cm
    ("90cm",
     np.array([6.62, 0.000, 0.10, 0.55, 1.00, 1.48, 1.92, 2.46, 2.99,
               3.32, 3.83, 4.27, 4.81, 5.28, 5.71, 6.12, 6.27, 6.34, 6.42, 6.48, 6.52, 6.57]),
     np.array([0, 32.44, 32.76, 32.48, 32.47, 32.48, 32.07, 31.44, 31.09,
               30.85, 30.34, 30.17, 29.88, 29.68, 29.28, 23.83, 19.33, 16.05, 12.33, 9.10, 6.59, 2.52])),

    # 75 cm
    ("75cm",
     np.array([3.417, 0.000, 0.849, 1.307, 1.531, 1.865, 2.323, 2.753, 2.993,
               0.549, 3.383, 0.320, 1.149, 2.010, 2.534, 3.096, 3.185, 3.219, 3.277, 3.316, 3.345, 3.365, 3.376]),
     np.array([0, 45.02, 44.98, 44.87, 44.80, 44.72, 44.56, 44.19, 42.03,
               45.03, 3.79, 45.16, 45.04, 44.97, 44.76, 38.65, 32.80, 29.09, 22.17, 16.69, 11.54, 7.70, 5.35])),

    # 60 cm
    ("60cm",
     np.array([3.39, 0.00, 0.12, 0.57, 1.04, 1.43, 1.67, 2.23, 3.02,
               3.21, 3.27, 3.31, 3.33, 3.35, 3.36, 3.37, 3.38, 1.76, 1.95, 2.16, 2.39, 2.82]),
     np.array([0, 41.52, 42.02, 41.92, 41.77, 41.48, 41.37, 41.18, 39.33,
               29.90, 22.20, 17.16, 13.46, 9.38, 7.55, 5.88, 3.42, 41.18, 41.22, 40.95, 40.86, 40.65])),

    # 两电池并联
    ("并联",
     np.array([3.350, 0.000, 0.382, 0.716, 1.039, 1.397, 1.819, 2.255, 2.633,
               2.875, 3.095, 3.154, 3.199, 3.233, 3.261, 3.283, 3.296, 3.314, 3.324, 3.332, 3.338, 3.352]),
     np.array([0, 58.26, 58.87, 58.77, 58.87, 59.20, 59.23, 58.87, 54.52,
               48.15, 36.40, 31.00, 26.04, 21.79, 17.66, 14.11, 11.91, 8.75, 6.90, 5.22, 4.03, 1.01])),

    # 两电池串联
    ("串联",
     np.array([6.66, 0, 0.57, 0.94, 1.57, 1.73, 1.95, 2.22, 2.46,
               2.66, 2.88, 3.16, 3.37, 3.47, 3.72, 4.10, 4.44, 4.88, 5.53, 5.93, 6.13, 6.28, 6.38, 6.44, 6.50, 6.56, 6.60, 6.69]),
     np.array([0, 33.91, 33.74, 33.72, 33.60, 33.85, 33.68, 33.67, 33.52,
               33.36, 33.39, 33.18, 33.11, 32.98, 32.88, 32.79, 32.66, 32.69, 32.34, 30.27, 27.34, 23.46, 19.62, 16.85, 13.80, 10.68, 7.84, 6.61])),

    # 两串两并
    ("2串2并",
     np.array([10.03, 0.00, 0.67, 1.35, 1.87, 2.31, 2.75, 3.28, 3.75,
               4.11, 4.55, 5.26, 6.00, 6.64, 7.59, 8.06, 8.42, 8.99, 9.34, 9.52, 9.66, 9.74, 9.80, 9.97]),
     np.array([0, 23.81, 23.48, 23.04, 22.87, 22.78, 22.54, 22.50, 22.43,
               22.30, 22.18, 22.05, 21.92, 21.80, 21.75, 21.63, 21.68, 21.53, 20.18, 17.84, 14.41, 11.90, 9.90, 2.78])),

    # 一串三并
    ("1串3并",
     np.array([6.62, 0.000, 0.10, 0.55, 1.00, 1.48, 1.92, 2.46, 2.99,
               3.32, 3.83, 4.27, 4.81, 5.28, 5.71, 6.12, 6.27, 6.34, 6.42, 6.48, 6.52, 6.57]),
     np.array([0, 32.44, 32.76, 32.48, 32.47, 32.48, 32.07, 31.44, 31.09,
               30.85, 30.34, 30.17, 29.88, 29.68, 29.28, 23.83, 19.33, 16.05, 12.33, 9.10, 6.59, 2.52])),
]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
colors = plt.cm.tab10(np.linspace(0, 1, len(datasets)))
all_V, all_I, all_Pmax = [], [], []

for (name, V_raw, I_raw), color in zip(datasets, colors):

    sort_idx = np.argsort(V_raw)
    V = V_raw[sort_idx]
    I = I_raw[sort_idx]
    I = np.minimum.accumulate(I)
    _, unique_idx = np.unique(V, return_index=True)
    V_unique = V[unique_idx]
    I_unique = I[unique_idx]
    V_max = V_unique[-1]
    V_extended = np.append(V_unique, V_max + 0.02)
    I_extended = np.append(I_unique, 0)
    f_interp = PchipInterpolator(V_extended, I_extended, extrapolate=False)
    V_dense = np.linspace(0, V_max + 0.02, 500)
    I_dense = f_interp(V_dense)
    I_dense = np.maximum(I_dense, 0)   # 确保无负电流
    if V[0] == 0:
        Isc = I[0]
    else:
        Isc = f_interp(0) if 0 >= V[0] else I[0]
    idx_zeros = np.where(I_dense <= 0)[0]
    if len(idx_zeros) > 0:
        idx = idx_zeros[0]
        if idx > 0:
            Voc = np.interp(0, I_dense[idx-1:idx+1][::-1], V_dense[idx-1:idx+1][::-1])
        else:
            Voc = V_dense[0]
    else:
        Voc = V_dense[-1]
    P_dense = V_dense * I_dense
    max_power_idx = np.argmax(P_dense)
    Vmp = V_dense[max_power_idx]
    Imp = I_dense[max_power_idx]
    Pmax = P_dense[max_power_idx]
    FF = Pmax / (Voc * Isc) if Voc * Isc != 0 else 0

    # 打印参数(可选)
    '''print(f"{name}:")
    print(f"  Isc = {Isc:.3f} mA, Voc = {Voc:.3f} V")
    print(f"  Vmp = {Vmp:.3f} V, Imp = {Imp:.3f} mA, Pmax = {Pmax:.3f} mW")
    print(f"  FF = {FF:.3f}\n")'''

    all_V.extend(V)
    all_I.extend(I)
    all_Pmax.append(Pmax)

    #I-V 曲线
    ax1.plot(V_dense, I_dense, color=color, linewidth=2,
             label=f"{name} (Isc={Isc:.1f} mA, Voc={Voc:.2f} V)")
    ax1.plot(Vmp, Imp, marker='*', markersize=10,
             color='white', markeredgecolor=color, markeredgewidth=1.5,
             zorder=10)
    ax1.text(Vmp + 0.02, Imp, f'{Pmax:.1f} mW', fontsize=8,
             color=color, verticalalignment='center')

    # P-V 曲线
    ax2.plot(V_dense, P_dense, color=color, linewidth=2,
             label=f"{name} (Pmax={Pmax:.1f} mW)")
    ax2.plot(Vmp, Pmax, marker='*', markersize=10,
             color='white', markeredgecolor=color, markeredgewidth=1.5,
             zorder=10)
    ax2.text(Vmp + 0.02, Pmax, f'{Pmax:.1f} mW', fontsize=8,
             color=color, verticalalignment='center')

ax1.set_xlabel('电压 (V)')
ax1.set_ylabel('电流 (mA)')
ax1.set_title('不同配置下的 I-V 曲线对比\n(★为最大功率点)')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='best', fontsize=8)
ax1.set_xlim(0, max(all_V) * 1.05)
ax1.set_ylim(0, max(all_I) * 1.05)

ax2.set_xlabel('电压 (V)')
ax2.set_ylabel('功率 (mW)')
ax2.set_title('不同配置下的 P-V 曲线对比\n(★为最大功率点)')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(loc='best', fontsize=8)
ax2.set_xlim(0, max(all_V) * 1.05)
ax2.set_ylim(0, max(all_Pmax) * 1.1)

plt.tight_layout()
plt.savefig('solar_cell_comparison_with_pmax_label.png', dpi=150)
plt.show()
