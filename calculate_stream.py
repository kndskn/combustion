from scipy.integrate import quad
from math import pi

R_1 = 12.7
R_2 = 17.4
def f_initial(r): return r
def f_smooth(r): return 1 / 4 * (R_1 - r) * (r - R_2) * r


def calc_cylinder_stream(func):
    """Calculates stream in cylinder system of coordinates"""
    i = 2 * pi * quad(func, R_1, R_2)[0]
    return i


if __name__ == '__main__':
    print(calc_cylinder_stream(f_initial))
    print(calc_cylinder_stream(f_smooth))
