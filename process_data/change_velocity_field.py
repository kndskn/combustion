import os
import numpy as np
from ast import literal_eval

path = '/test'
path_points = '/test/points'


def read_points(path):
    """Read points from file
    :return: radiuses of points"""
    x = []
    r = []
    with open(path, 'r') as f:
        m = 0
        for line in f:
            if m > 2 and line.strip() != ')':
                vect = line.strip()
                vect = vect.replace(' ', ',')
                vect = np.array(literal_eval(vect))
                x.append(vect)
            m += 1
    for i in range(len(x)):
        r[i] = (x[i][0] ** 2 + x[i][1] ** 2) ** (1 / 2)
    return r


def read_vel(path, filename):
    v = []
    cur_dir = os.path.join(path, filename)
    if os.path.isdir(cur_dir):
        with open(cur_dir + '/U', 'r') as f:
            m = 0
            for line in f:
                if m > 2 and line.strip() != ')':
                    vect = line.strip()
                    vect = vect.replace(' ', ',')
                    vect = np.array(literal_eval(vect))
                    v.append(vect)
                m += 1
            v = np.array(v)
    return v


def average_velocity(path):
    i = 0
    v_full = []
    for filename in list(reversed(os.listdir(path))):
        v_full.append(read_vel(path, filename))
        i += 1
    v_sum = v_full[1]
    for j in range(2, i, 1):
        v_sum += v_full[j]
    return v_sum / 31600


def write_new_vel(v, v_mean, path, r):
    c = r
    for filename in list(reversed(os.listdir(path))):
        cur_dir = os.path.join(path, filename)
        v_new = (v - v_mean) * c + v_mean
        with open(cur_dir + '/U', 'w') as f:
            f.write('\n')
            f.write('31600\n')
            f.write('(\n')
            for i in range(len(v_new)):
                vect = str(v_new[i]).replace('[', '(')
                vect = vect.replace(']', ')')
                vect = vect.replace(',', ' ') + '\n'
                f.write(vect)
            f.write(')\n')


def main():
    # np.set_printoptions(threshold=sys.maxsize)
    v_mean = average_velocity(path)
    # r = read_points(path_points)
    for filename in os.listdir(path):
        v = (read_vel(path, filename))
        write_new_vel(v, v_mean, path, r=0.66)


if __name__ == '__main__':
    main()
