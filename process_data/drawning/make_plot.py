import numpy as np
import matplotlib.pyplot as plt
from process_data import calculate_stream
from process_data.parameters import *
from process_data import own_mpl_style_module as own
from process_data import latex_document_parameters as latex
from matplotlib.offsetbox import AnchoredText

own.matplotlib_header()


def fill_array(inp, w_exp_file, uv_exp_file, z_label):
    x, y, z, u, v, w, uu, vv, ww, uv, uw, vw = np.loadtxt(inp,
                                                          usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
                                                          delimiter='\t',
                                                          skiprows=1,
                                                          unpack=True)
    u_exp2 = np.zeros(z.size)
    v_exp2 = np.zeros(z.size)
    w_exp2 = np.zeros(z.size)
    uu_exp2 = np.zeros(z.size)
    vv_exp2 = np.zeros(z.size)
    ww_exp2 = np.zeros(z.size)
    r_exp2 = np.zeros(z.size)
    r_exp_w2 = np.zeros(z.size)

    r_exp_w1, w_exp1, ww_exp1 = np.loadtxt(w_exp_file, usecols=(0, 2, 3), delimiter='\t', skiprows=1, unpack=True)
    r_exp1, u_exp1, v_exp1, uu_exp1, vv_exp1 = np.loadtxt(uv_exp_file, usecols=(0, 2, 4, 3, 5), delimiter='\t',
                                                          skiprows=1, unpack=True)
    n = 0

    for i in range(r_exp1.size):
        if r_exp1[i] < 0:
            r_exp2[n] = r_exp1[i] * (-1)
            r_exp1[i] = 0
            u_exp2[n] = u_exp1[i]
            u_exp1[i] = 0
            v_exp2[n] = (-1) * v_exp1[i]
            v_exp1[i] = 0
            # uu_exp2[n] = uu_exp1[i]
            uu_exp1[i] = 0
            # vv_exp2[n] = vv_exp1[i]
            vv_exp1[i] = 0
            n = n + 1

    n = 0

    for i in range(r_exp_w1.size):
        if r_exp_w1[i] < 0:
            r_exp_w2[n] = r_exp_w1[i] * (-1)
            r_exp_w1[i] = 0
            w_exp2[n] = (-1) * w_exp1[i]
            w_exp1[i] = 0
            # ww_exp2[n] = ww_exp1[i]
            ww_exp1[i] = 0
            n = n + 1

    r_exp1 = r_exp1 / D_r / 1e+3
    r_exp_w1 = r_exp_w1 / D_r / 1e+3
    r_exp2 = r_exp2 / D_r / 1e+3
    r_exp_w2 = r_exp_w2 / D_r / 1e+3

    w_exp1 = w_exp1 / Ub_r
    u_exp1 = u_exp1 / Ub_r
    v_exp1 = v_exp1 / Ub_r
    w_exp2 = w_exp2 / Ub_r
    u_exp2 = u_exp2 / Ub_r
    v_exp2 = v_exp2 / Ub_r

    ww_exp1 = (ww_exp1 / Ub_r) ** 2
    uu_exp1 = (uu_exp1 / Ub_r) ** 2
    vv_exp1 = (vv_exp1 / Ub_r) ** 2
    ww_exp2 = (ww_exp2 / Ub_r) ** 2
    uu_exp2 = (uu_exp2 / Ub_r) ** 2
    vv_exp2 = (vv_exp2 / Ub_r) ** 2
    u_r = np.zeros(z.size)
    v_r = np.zeros(z.size)
    w_r = np.zeros(z.size)

    uu_r = np.zeros(z.size)
    vv_r = np.zeros(z.size)
    ww_r = np.zeros(z.size)

    r = np.zeros(z.size)
    z_const = np.round(z_label / D_r, 2)

    m = 0
    for i in range(z.size):
        if z[i] == z_const:
            # u наше radial (v в эксперименте)
            # v наше tangential (w в эксперименте)
            # w наше axial (u в эскперименте)

            v_r[m] = v[i]
            u_r[m] = u[i]
            w_r[m] = w[i]
            if not np.isnan(vv[i]):
                vv_r[m] = (vv[i] + v[i] ** 2)
            if not np.isnan(uu[i]):
                uu_r[m] = (uu[i] + u[i] ** 2)
            if not np.isnan(ww[i]):
                ww_r[m] = ww[i]  # (ww[i] + w[i] ** 2)
            r[m] = x[m]
            m = m + 1

    output = dict(x=x, y=y, z=z, z_const=z_const, v_r=v_r, v=v, u_r=u_r, u=u, w_r=w_r, vv_r=vv_r, uu_r=uu_r, ww_r=ww_r,
                  w=w, r=r, r_exp1=r_exp1,
                  r_exp_w1=r_exp_w1, r_exp2=r_exp2, r_exp_w2=r_exp_w2, w_exp1=w_exp1, u_exp1=u_exp1, v_exp1=v_exp1,
                  w_exp2=w_exp2, u_exp2=u_exp2, v_exp2=v_exp2, ww_exp1=ww_exp1, uu_exp1=uu_exp1, vv_exp1=vv_exp1,
                  ww_exp2=ww_exp2, uu_exp2=uu_exp2, vv_exp2=vv_exp2, z_label=z_label)
    return output


def write_points_and_made_plot(inp_array, LES_mean, EXP_mean, LES_rms, EXP_rms, MODEL, limits_mean, limits_rms, name):
    v_r = np.array(inp_array.get('v_r'))
    u_r = np.array(inp_array.get('u_r'))
    w_r = np.array(inp_array.get('w_r'))

    vv_r = np.array(inp_array.get('vv_r'))
    uu_r = np.array(inp_array.get('uu_r'))
    ww_r = np.array(inp_array.get('ww_r'))

    r = np.array(inp_array.get('r'))
    r_exp1 = np.array(inp_array.get('r_exp1'))
    r_exp_w1 = np.array(inp_array.get('r_exp_w1'))
    r_exp2 = np.array(inp_array.get('r_exp2'))
    r_exp_w2 = np.array(inp_array.get('r_exp_w2'))

    w_exp1 = np.array(inp_array.get('w_exp1'))
    u_exp1 = np.array(inp_array.get('u_exp1'))
    v_exp1 = np.array(inp_array.get('v_exp1'))
    w_exp2 = np.array(inp_array.get('w_exp2'))
    u_exp2 = np.array(inp_array.get('u_exp2'))
    v_exp2 = np.array(inp_array.get('v_exp2'))

    ww_exp1 = np.array(inp_array.get('ww_exp1'))
    uu_exp1 = np.array(inp_array.get('uu_exp1'))
    vv_exp1 = np.array(inp_array.get('vv_exp1'))
    ww_exp2 = np.array(inp_array.get('ww_exp2'))
    uu_exp2 = np.array(inp_array.get('uu_exp2'))
    vv_exp2 = np.array(inp_array.get('vv_exp2'))

    z_label = np.array(inp_array.get('z_label'))

    # fig, ax = plt.subplots(1, 1, figsize=[8000. / 300, 8000. / 300])
    fig, ax = plt.subplots(1, 1, figsize=own.set_fig_size(latex.TEXT_WIDTH, 0.5))

    smooth_func = calculate_stream.made_array(calculate_stream.f_smooth_final, r)
    plt.subplots_adjust(left=0.12, bottom=0.12, wspace=0.)

    if LES_mean:
        ax.plot(r, v_r, color='red', marker='', mfc='w', label='LES tangential')
        ax.plot(r, w_r, color='green', marker='', mfc='w', label='LES axial')
        ax.plot(r, u_r, color='black', marker='', mfc='w', label='LES radial')

    if EXP_mean:
        ax.plot(r_exp_w1, w_exp1, color='red', marker='.', linestyle='', label='EXP tangential')
        ax.plot(r_exp_w2, w_exp2, color='red', marker='.', linestyle='')

        ax.plot(r_exp1, u_exp1, color='green', marker='.', linestyle='', label='EXP axial')
        ax.plot(r_exp2, u_exp2, color='green', marker='.', linestyle='')

        ax.plot(r_exp1, v_exp1, color='black', marker='.', linestyle='', label='EXP radial')
        ax.plot(r_exp2, v_exp2, color='orange', marker='.', linestyle='')

    if LES_rms:
        ax.plot(r, vv_r, color='red', marker='', mfc='w', label='LES RMS tangential')
        ax.plot(r, ww_r, color='green', marker='', mfc='w', label='LES RMS axial')
        ax.plot(r, uu_r, color='black', marker='', mfc='w', label='LES RMS radial')

    if EXP_rms:
        ax.plot(r_exp_w1, ww_exp1, color='red', marker='', linestyle=':', label='EXP RMS tangential')
        ax.plot(r_exp_w2, ww_exp2, color='red', marker='', linestyle=':')

        ax.plot(r_exp1, uu_exp1, color='green', marker='', linestyle=':', label='EXP RMS axial')
        ax.plot(r_exp2, uu_exp2, color='green', marker='', linestyle=':')

        ax.plot(r_exp1, vv_exp1, color='black', marker='', linestyle=':', label='EXP RMS radial')
        ax.plot(r_exp2, vv_exp2, color='black', marker='', linestyle=':')

    # if MODEL:
    #     ax.plot(r, smooth_func, color='black', marker='o', ms=10, mfc='w', linewidth=10,
    #             label='ANALYTIC_DES')

    ax.set_xlim([0, 0.55])

    if limits_mean:
        ax.set_ylim([-0.25, 1.3])
        # ax.set_ylabel(r'$U / U_b$')
        atext = AnchoredText(r'$U / U_b$',
                             loc='upper left',
                             pad=0.25,
                             borderpad=0.,
                             bbox_to_anchor=(0, 1),
                             bbox_transform=ax.transAxes,
                             frameon=True)
        ax.add_artist(atext)

    if limits_rms:
        ax.set_ylim([0, 0.06])
        # ax.set_ylabel('U\'\' U\'\' / (U_b * U_b)')
        # ax.set_ylabel(r'$\overline{U^\prime U^\prime} / U_b^2$')
        atext = AnchoredText(r'$\overline{U^\prime U^\prime} / U_b^2$',
                             loc='upper left',
                             pad=0.1,
                             borderpad=0.,
                             bbox_to_anchor=(0, 1),
                             bbox_transform=ax.transAxes,
                             frameon=True)
        ax.add_artist(atext)

    for axis in ['top', 'bottom', 'left', 'right']:
        # ax.spines[axis].set_linewidth(5)
        ax.spines[axis].set_zorder(0)

    # ax.tick_params(axis='both',  # Применяем параметры к обеим осям
    #                which='major',  # Применяем параметры к основным делениям
    #                direction='inout',  # Рисуем деления внутри и снаружи графика
    #                length=20,  # Длинна делений
    #                width=4,  # Ширина делений
    #                color='m',  # Цвет делений
    #                pad=10,  # Расстояние между черточкой и ее подписью
    #                labelsize=40,  # Размер подписи
    #                bottom=True,  # Рисуем метки снизу
    #                left=True,  # слева
    #                labelbottom=True,  # Рисуем подписи снизу
    #                labelleft=True)

    # ax.legend(fontsize=50)
    __txt = str(np.round(z_label / D_r, 2))
    # ax.set_title(r'$z / D = ' + __txt + '$')
    atext = AnchoredText(r'$z / D = ' + __txt + '$',
                         loc='upper center',
                         pad=0.1,
                         borderpad=0.,
                         bbox_to_anchor=(0.5, 1),
                         bbox_transform=ax.transAxes,
                         frameon=True)
    ax.add_artist(atext)
    # ax.set_xlabel(r'$r / D$')
    atext = AnchoredText(r'$r / D$',
                         loc='lower center',
                         pad=0.1,
                         borderpad=0.,
                         bbox_to_anchor=(0.5, 0),
                         bbox_transform=ax.transAxes,
                         frameon=True)
    ax.add_artist(atext)
    fig.tight_layout()
    plt.savefig('./pictures/' + f'{name}')
    plt.show()
