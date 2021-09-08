from scipy.integrate import quad
from math import pi

D_r = 38.1
R_1 = 12.7 / D_r
R_2 = 17.4 / D_r
C_4 = 0.02
C_5 = 0.02
C_1 = -1711.31 - 16.469 * C_4 - 126.881 * C_5
C_2 = 1351.93 + 19.5982 * C_4 + 134.519 * C_5
C_3 = -259.777 - 7.70422 * C_4 - 39.7568 * C_5


def f_initial_for_q(r): return 1. * r


def f_smooth_for_q_1(r): return 1.2e4 / 40 * (R_1 - r) * (r - R_2) * r
def f_smooth_1(r): return 1.2e4 / 40 * (R_1 - r) * (r - R_2)


def f_smooth_for_q_2(r): return (-7e4 * (r - 0.395) ** 4 + 1.15) * r
def f_smooth_2(r): return -7e4 * ((r - 0.395) ** 4) + 1.15

def f_smooth_for_q_3(r):
    return (C_1 * r ** 4 + C_2 * r ** 3 + C_3 * r ** 2 + C_4 * r + C_5) * r
def f_smooth_3(r): return C_1 * r ** 4 + C_2 * r ** 3 + C_3 * r ** 2 + C_4 * r + C_5


def f_smooth_for_q_final(r): return f_smooth_for_q_3(r)
def f_smooth_final(r): return f_smooth_3(r)


def calc_cylinder_stream(func):
    """Calculates stream in cylinder system of coordinates"""
    i = 2 * pi * quad(func, R_1, R_2)[0]
    return i


def made_array(func, points):
    """Take your function and made array of points from it"""
    data = []
    for i in range(len(points)):
        data.append(func(points[i]))
    return data


if __name__ == '__main__':
    print(calc_cylinder_stream(f_initial_for_q))
    print(calc_cylinder_stream(f_smooth_for_q_final))
