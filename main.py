import matplotlib.pyplot as plt
import numpy as np
import calculate_stream

# Choose input data and default arrays
z_label = 2
Ub = 18.7
D_r = 38.1


input_file = 'from_paraview_u_mean_noswirl_average_data_to_2d_matplotlib.tsv'
w_exp_file = 'exp_data/cSwB1_ns_z' + str(z_label) + '_W_MeanAndRMS.txt'
uv_exp_file = 'exp_data/cSwB1_ns_z' + str(z_label) + '_UV_MeanAndRMS.txt'

x, z, y, u, w, v, uu, ww, vv, uw, uv, vw = np.loadtxt(input_file,
                                                      usecols=(0, 2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11),
                                                      delimiter='\t',
                                                      skiprows=1,
                                                      unpack=True)
u_exp2 = np.zeros(z.size)
v_exp2 = np.zeros(z.size)
w_exp2 = np.zeros(z.size)
r_exp2 = np.zeros(z.size)
r_exp_w2 = np.zeros(z.size)

r_exp_w1, w_exp1 = np.loadtxt(w_exp_file, usecols=(0, 2), delimiter='\t', skiprows=1, unpack=True)
r_exp1, u_exp1, v_exp1 = np.loadtxt(uv_exp_file, usecols=(0, 2, 4), delimiter='\t', skiprows=1, unpack=True)
n = 0

for i in range(r_exp1.size):
    if r_exp1[i] < 0:
        r_exp2[n] = r_exp1[i] * (-1)
        u_exp2[n] = u_exp1[i]
        v_exp2[n] = (-1) * v_exp1[i]
        n = n + 1

n = 0

for i in range(r_exp_w1.size):
    if r_exp_w1[i] < 0:
        r_exp_w2[n] = r_exp_w1[i] * (-1)
        w_exp2[n] = (-1) * w_exp1[i]
        n = n + 1


r_exp1 = r_exp1 / D_r
r_exp_w1 = r_exp_w1 / D_r
r_exp2 = r_exp2 / D_r
r_exp_w2 = r_exp_w2 / D_r
w_exp1 = w_exp1 / Ub
u_exp1 = u_exp1 / Ub
v_exp1 = v_exp1 / Ub
w_exp2 = w_exp2 / Ub
u_exp2 = u_exp2 / Ub
v_exp2 = v_exp2 / Ub
u_r = np.zeros(z.size)
v_r = np.zeros(z.size)
w_r = np.zeros(z.size)
r = np.zeros(z.size)
m = 0

z_const = np.round(z_label / D_r, 2)

# Write needed dots to matplotlib

for i in range(z.size):
    if y[i] == z_const:

        # u наше radial (v в эксперименте)
        # w наше axial (u в эскперименте)
        # v наше tangential (w в эксперименте)

        v_r[m] = v[i]
        u_r[m] = u[i]
        w_r[m] = w[i]
        r[m] = x[m]
        m = m + 1

fig, ax = plt.subplots(1, 1, figsize=[8000. / 300, 8000. / 300])

smooth_func = calculate_stream.made_array(calculate_stream.f_smooth_final, r)

# Tune subplot layout

plt.subplots_adjust(left=0.12, bottom=0.12, wspace=0.)
# ax.plot(r, v_r, color='red', marker='o', ms=10, mfc='w', mew=0.5, linewidth=10, label='LES tangential')
ax.plot(r, w_r, color='violet', marker='o', ms=10, mfc='w', mew=0.5, linewidth=10, label='LES axial')
# ax.plot(r, u_r, color='teal', marker='o', ms=10, mfc='w', mew=0.5, linewidth=10, label='LES radial')
# ax.plot(r_exp_w1, w_exp1, color='green', marker='o', linewidth=10, linestyle=':', label='EXP tangential')
ax.plot(r_exp1, u_exp1, color='blue', marker='o', linewidth=10, linestyle=':', label='EXP axial')
# ax.plot(r_exp1, v_exp1, color='orange', marker='o', linewidth=10, linestyle=':', label='EXP radial')
# ax.plot(r_exp_w2, w_exp2, color='green', marker='o', linewidth=10, linestyle=':')
# ax.plot(r_exp2, u_exp2, color='blue', marker='o', linewidth=10, linestyle=':')
# ax.plot(r_exp2, v_exp2, color='orange', marker='o', linewidth=10, linestyle=':')
ax.plot(r, smooth_func, color='black', marker='o', ms=10, mfc='w', mew=0.5, linewidth=10, label='ANALYTIC_DES')
ax.set_xlim([0, 0.8])
ax.set_ylim([-0.2, 1.8])
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(5)
    ax.spines[axis].set_zorder(0)
ax.tick_params(axis='both',  # Применяем параметры к обеим осям
               which='major',  # Применяем параметры к основным делениям
               direction='inout',  # Рисуем деления внутри и снаружи графика
               length=20,  # Длинна делений
               width=4,  # Ширина делений
               color='m',  # Цвет делений
               pad=10,  # Расстояние между черточкой и ее подписью
               labelsize=40,  # Размер подписи
               bottom=True,  # Рисуем метки снизу
               left=True,  # слева
               labelbottom=True,  # Рисуем подписи снизу
               labelleft=True)
ax.legend(fontsize=50)
ax.set_title('z = ' + str(z_label), fontsize=60)
ax.set_xlabel('R', fontsize=60)
fig.tight_layout()
print('Q_initial = ', calculate_stream.calc_cylinder_stream(calculate_stream.f_initial_for_q))
print('Q_present = ', calculate_stream.calc_cylinder_stream(calculate_stream.f_smooth_for_q_final))
plt.show()
