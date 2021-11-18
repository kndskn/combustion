from scipy.integrate import quad
from math import pi
import matplotlib.pyplot as plt

# Declaration of constants

R_1 = 12.7 * 1e-3
R_2 = 18.3 * 1e-3
C_4 = 0.02
C_5 = 0.02
C_1 = -1711.31 - 16.469 * C_4 - 126.881 * C_5
C_2 = 1351.93 + 19.5982 * C_4 + 134.519 * C_5
C_3 = -259.777 - 7.70422 * C_4 - 39.7568 * C_5
p = [i / 100000 for i in range(18000)]


def calc_cylinder_stream(func):
    """Calculates stream in cylinder system of coordinates"""
    i = 2 * pi * quad(func, R_1, R_2)[0]
    return i


def make_array(func, points):
    """Take your function and made array of points from it"""
    data = []
    for i in range(len(points)):
        data.append(func(points[i]))
    return data


def f_initial_for_q(r): return 8.3 * r


def f_smooth_for_q_1(r): return 1.2e4 / 40 * (R_1 - r) * (r - R_2) * r


def f_smooth_1(r): return 1.2e4 / 40 * (R_1 - r) * (r - R_2)


def f_smooth_for_q_2(r): return (-7e4 * (r - 0.395) ** 4 + 1.15) * r


def f_smooth_2(r): return -7e4 * ((r - 0.395) ** 4) + 1.15


def f_smooth_for_q_3(r):
    return (C_1 * r ** 4 + C_2 * r ** 3 + C_3 * r ** 2 + C_4 * r + C_5) * r


def f_smooth_3(r): return C_1 * r ** 4 + C_2 * r ** 3 + C_3 * r ** 2 + C_4 * r + C_5


Q = calc_cylinder_stream(f_initial_for_q)
gamma = (6 * Q * R_1 ** 2 * R_2 ** 2) / pi / ((R_1 ** 2 - R_2 ** 2) ** 3)
alpha = -(gamma / (R_1 ** 2 * R_2 ** 2))
beta = ((R_1 ** 2 + R_2 ** 2) * gamma) / (R_1 ** 2 * R_2 ** 2)


def f_smooth_for_q_4(r): return (- alpha * r ** 4 - beta * r ** 2 + gamma) * r


def f_smooth_4(r): return - alpha * r ** 4 - beta * r ** 2 + gamma


a2 = - (7 * Q) / (6 * pi * (R_1 - R_2) * (R_1 + R_2))


def f_smooth_for_q_6(r): return a2 * (1 - (-(2 / (R_1 - R_2)) * r - (-R_1 - R_2) / (R_1 - R_2)) ** 6) * r


def f_smooth_6(r): return a2 * (1 - (-(2 / (R_1 - R_2)) * r - (-R_1 - R_2) / (R_1 - R_2)) ** 6)


def f_smooth_for_q_final(r): return f_smooth_for_q_1(r)


def f_smooth_final(r): return f_smooth_1(r)


if __name__ == '__main__':
    print('Q_initial = ', calc_cylinder_stream(f_initial_for_q))
    print('Q_present = ', calc_cylinder_stream(f_smooth_for_q_final))
    fig, ax = plt.subplots(1, 1, figsize=[8000. / 300, 8000. / 300])
    smooth_func = make_array(f_smooth_final, p)
    plt.subplots_adjust(left=0.12, bottom=0.12, wspace=0.)
    ax.plot(p, smooth_func, color='black',  ms=10, mfc='w', mew=0.5, linewidth=10,
            label='ANALYTIC_DES')
    ax.set_xlim([0.001, 0.02])
    ax.set_ylim([-0.2, 25])
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
    ax.set_xlabel('R', fontsize=60)
    fig.tight_layout()
    plt.show()
