from scipy.integrate import quad
from math import pi
from parameters import *


def calc_cylinder_stream(func, r1, r2):
    """Calculates stream in cylinder system of coordinates"""
    i = 2 * pi * quad(func, r1, r2)[0]
    return i


def made_array(func, points):
    """Take your function and made array of points from it"""
    data = []
    for i in range(len(points)):
        data.append(func(points[i]))
    return data


def f_initial_for_q(r): return U_o / Ub_r * r


def f_initial_for_q_inner(r): return U_i / Ub_r * r


Q = calc_cylinder_stream(f_initial_for_q, R_1, R_2)
Q_i = calc_cylinder_stream(f_initial_for_q_inner, R_1_inner, R_2_inner)
gamma = (6 * Q * R_1 ** 2 * R_2 ** 2) / pi / ((R_1 ** 2 - R_2 ** 2) ** 3)
alpha = -(gamma / (R_1 ** 2 * R_2 ** 2))
beta = ((R_1 ** 2 + R_2 ** 2) * gamma) / (R_1 ** 2 * R_2 ** 2)
a2 = - (7 * Q) / (6 * pi * (R_1 - R_2) * (R_1 + R_2))
a3 = - (7 * Q_i) / (6 * pi * (R_1_inner - R_2_inner) * (R_1_inner + R_2_inner))
a4 = (6 * Q_i) / (pi * (R_1_inner - R_2_inner) ** 3 * (R_1_inner + R_2_inner))


def f_smooth_for_q_1(r): return a4 * (r - R_1_inner) * (r - R_2_inner) * r


def f_smooth_1(r): return a4 * (r - R_1_inner) * (r - R_2_inner)


def f_smooth_for_q_2(r): return (-7e4 * (r - 0.395) ** 4 + 1.15) * r


def f_smooth_2(r): return -7e4 * ((r - 0.395) ** 4) + 1.15


def f_smooth_for_q_3(r):
    return (C_1 * r ** 4 + C_2 * r ** 3 + C_3 * r ** 2 + C_4 * r + C_5) * r


def f_smooth_3(r): return C_1 * r ** 4 + C_2 * r ** 3 + C_3 * r ** 2 + C_4 * r + C_5


def f_smooth_for_q_4(r): return (- alpha * r ** 4 - beta * r ** 2 + gamma) * r


def f_smooth_4(r): return - alpha * r ** 4 - beta * r ** 2 + gamma


def f_smooth_for_q_6(r): return a2 * (1 - (-(2 / (R_1 - R_2)) * r - (-R_1 - R_2) / (R_1 - R_2)) ** 6) * r


def f_smooth_6(r): return a2 * (1 - (-(2 / (R_1 - R_2)) * r - (-R_1 - R_2) / (R_1 - R_2)) ** 6)


def f_smooth_for_q_7(r): return a3 * (1 - (-(2 / (R_1_inner - R_2_inner)) * r -
                                           (-R_1_inner - R_2_inner) / (R_1_inner - R_2_inner)) ** 6) * r


def f_smooth_7(r): return a3 * (1 - (-(2 / (R_1_inner - R_2_inner)) * r - (-R_1_inner - R_2_inner) / (R_1_inner - R_2_inner)) ** 6)


def f_smooth_for_q_final(r): return f_smooth_for_q_1(r)


def f_smooth_final(r): return f_smooth_1(r)


if __name__ == '__main__':
    print(Q_i)
    print(calc_cylinder_stream(f_smooth_for_q_final, R_1_inner, R_2_inner))
