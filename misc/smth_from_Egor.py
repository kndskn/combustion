#!/bin/python2

# LES data from shallow cylinder flow in 2d z-slice on half height.
# Data is triangulated and plotted with streamlines

# import own_matplotlib_style_module as own
import numpy as np
from matplotlib.offsetbox import AnchoredText
from os import system
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.patches as patches
from plot_parameters_matplotlib_exp_and_sim import *
from comb_data_2d_structured import *

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# --------------- -------------------------------------------------------------
# Structured grid for experiment [left plot]
# --------------- -------------------------------------------------------------

# x and y vectors for streamplot
Xli = np.linspace(x_min_l, x_max_l, n_grid_x_l)
Yli = np.linspace(y_min, y_max, n_grid_y_l)

x_l = np.reshape(x_l, (n_grid_y_l, n_grid_x_l))
y_l = np.reshape(y_l, (n_grid_y_l, n_grid_x_l))
u_l = np.reshape(u_l, (n_grid_y_l, n_grid_x_l))
v_l = np.reshape(v_l, (n_grid_y_l, n_grid_x_l))
w_l = np.reshape(w_l, (n_grid_y_l, n_grid_x_l))
c1_l = np.reshape(np.zeros(np.size(uu_l)), (n_grid_y_l, n_grid_x_l))
uu_l = np.reshape(uu_l, (n_grid_y_l, n_grid_x_l))
vv_l = np.reshape(vv_l, (n_grid_y_l, n_grid_x_l))
ww_l = np.reshape(ww_l, (n_grid_y_l, n_grid_x_l))
uv_l = np.reshape(uv_l, (n_grid_y_l, n_grid_x_l))
uw_l = np.reshape(uw_l, (n_grid_y_l, n_grid_x_l))
vw_l = np.reshape(vw_l, (n_grid_y_l, n_grid_x_l))

print(np.shape(x_l))

# --------------- -------------------------------------------------------------
# Structured grid for simulation [right plot]
# --------------- -------------------------------------------------------------

# x and y vectors for streamplot
Xri = np.linspace(x_min_r, x_max_r, n_grid_x_r)
Yri = np.linspace(y_min, y_max, n_grid_y_r)

x_r = np.reshape(x_r, (n_grid_y_r, n_grid_x_r))
y_r = np.reshape(y_r, (n_grid_y_r, n_grid_x_r))
z_r = np.reshape(z_r, (n_grid_y_r, n_grid_x_r))
u_r = np.reshape(u_r, (n_grid_y_r, n_grid_x_r))
v_r = np.reshape(v_r, (n_grid_y_r, n_grid_x_r))
w_r = np.reshape(w_r, (n_grid_y_r, n_grid_x_r))
c1_r = np.reshape(c1_r, (n_grid_y_r, n_grid_x_r))
uu_r = np.reshape(uu_r, (n_grid_y_r, n_grid_x_r))
vv_r = np.reshape(vv_r, (n_grid_y_r, n_grid_x_r))
ww_r = np.reshape(ww_r, (n_grid_y_r, n_grid_x_r))
uv_r = np.reshape(uv_r, (n_grid_y_r, n_grid_x_r))
uw_r = np.reshape(uw_r, (n_grid_y_r, n_grid_x_r))
vw_r = np.reshape(vw_r, (n_grid_y_r, n_grid_x_r))

print(np.shape(x_r))

# --------------- -------------------------------------------------------------
# Vars to plot
# --------------- -------------------------------------------------------------
vars_v_l = [u_l, v_l, -w_l, uu_l, vv_l, ww_l, uv_l, uw_l, vw_l, c1_l]
vars_v_r = [-u_r, v_r, w_r, uu_r, vv_r, ww_r, -uv_r, uw_r, -vw_r, c1_r]

vars_m = [-1, -1, 0.0, 0., 0., 0., -0.8, -0.9, -1., 0.]
vars_M = [1, 3, 2.5, 2., 2.5, 4.5, 0.8, 1.2, 0.8, 1.]

vars_c = [r'$\bar{u}_r$',
          r'$\bar{u}_x$',
          r'$\bar{u}_\varphi$',
          r'$\overline{u^\prime_ru^\prime_r}$',
          r'$\overline{u^\prime_xu^\prime_x}$',
          r'$\overline{u^\prime_\varphi u^\prime_\varphi}$',
          r'$\overline{u^\prime_ru^\prime_x}$',
          r'$\overline{u^\prime_ru^\prime_\varphi}$',
          r'$\overline{u^\prime_xu^\prime_\varphi}$', 'c'
          ]
vars_f = ['U', 'V', 'W', 'uu', 'vv', 'ww', 'uv', 'uw', 'vw', 'c']
vars_t = ['k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k']

for k in range(len(vars_v_r)):
    print('Working on: {}'.format(vars_c[k]))
    print('left  var_min: {0: 5.1e} var_max: {1: 5.1e}'.
          format(np.min(vars_v_l[k]), np.max(vars_v_l[k])))

    # for plotting
    z_min = vars_m[k]
    z_max = vars_M[k]
    z_levels = 20
    z_range = np.linspace(z_min, z_max, num=z_levels)

    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(1, 2,
                           figsize=[3508. / 300, 2480. / 300])

    # Tune subplot layout, hspace for h interval
    plt.subplots_adjust(left=0.12, bottom=0.12, wspace=0.)
    # -------------------------------------------------------------------------

    cntr = ax[0].contourf(x_l, y_l, vars_v_l[k],
                          levels=z_range,
                          extend='both')

    strm = ax[0].streamplot(x_l, y_l, u_l, v_l,
                            zorder=1,
                            color='w',
                            density=50,
                            start_points=seed_points_l.T)

    # on this axes
    ax[0].axis([x_min_l, x_max_l, y_min, y_max])

    # Set scale x:y = 1 by tweaking the margins
    ax[0].set_aspect('equal', adjustable='box')

    # Define MTL
    x_ticks = np.arange(start=xl_min_l, stop=xl_max_l + dxl / 2, step=dxl)
    y_ticks = np.arange(start=yl_min, stop=yl_max + dyl / 2, step=dyl)

    # Number of minor ticks between major ticks
    ax[0].xaxis.set_minor_locator(AutoMinorLocator(n=int(5 + 1)))
    ax[0].yaxis.set_minor_locator(AutoMinorLocator(n=int(5 + 1)))

    # Set MTL
    ax[0].xaxis.set_ticks(x_ticks)
    ax[0].yaxis.set_ticks(y_ticks)

    # Tick colors
    ax[0].tick_params(axis='both', which='both', color=vars_t[k])

    atext = AnchoredText(r'$PIV$',
                         loc='upper left',
                         pad=0.15,
                         borderpad=0.,
                         frameon=True)
    ax[0].add_artist(atext)

    # atext = AnchoredText(vars_c[k],
    #                      loc='upper right',
    #                      pad=0.15,
    #                      borderpad=0.,
    #                      frameon=True)
    # ax[0].add_artist(atext)

    # -------------------------------------------------------------------------

    print('right var_min: {0: 5.1e} var_max: {1: 5.1e}'.
          format(np.min(vars_v_r[k]), np.max(vars_v_r[k])))

    cntr = ax[1].contourf(x_r, y_r, vars_v_r[k],
                          levels=z_range,
                          extend='both')

    strm = ax[1].streamplot(Xri, Yri, u_r, v_r,
                            zorder=1,
                            color='w',
                            density=50,
                            start_points=seed_points_r.T)

    # on this axes
    ax[1].axis([x_min_r, x_max_r, y_min, y_max])

    # Set scale x:y = 1 by tweaking the margins
    ax[1].set_aspect('equal', adjustable='box')

    # Define MTL
    x_ticks = np.arange(start=xl_min_r, stop=xl_max_r + dxl / 2, step=dxl)
    y_ticks = np.arange(start=yl_min, stop=yl_max + dyl / 2, step=dyl)

    # Number of minor ticks between major ticks
    ax[1].xaxis.set_minor_locator(AutoMinorLocator(n=int(5 + 1)))
    ax[1].yaxis.set_minor_locator(AutoMinorLocator(n=int(5 + 1)))

    # Set MTL
    ax[1].xaxis.set_ticks(x_ticks)
    # ax[1].yaxis.set_ticks(y_ticks)

    # Render MTL on canvas
    fig.canvas.draw()
    xlabel = [k.get_text() for k in ax[1].get_xticklabels()]
    ylabel = [k.get_text() for k in ax[1].get_yticklabels()]

    # Overwrite them
    xlabel[0] = ''
    ylabel = [''] * len(y_ticks)

    # Apply settings above
    ax[1].set_xticklabels(xlabel)
    ax[1].set_yticklabels(ylabel)

    ax[1].set_yticklabels([''] * len(y_ticks))

    # Tick colors
    ax[1].tick_params(axis='both', which='both', color=vars_t[k])

    atext = AnchoredText(r'$LES$',
                         loc='upper left',
                         pad=0.15,
                         borderpad=0.,
                         frameon=True)
    ax[1].add_artist(atext)

    # ------------------------------------------------------------ #
    # Default white box height [pix]
    wboxh = 213

    # White box
    wbox = inset_axes(ax[1], '45%', wboxh / fig.dpi,
                      loc='upper right',
                      borderpad=0.0,
                      bbox_to_anchor=(.033, 0., 1, 1),
                      bbox_transform=ax[1].transAxes)
    wbox.axis('off')
    rect = patches.Rectangle(
        (0, 0), 1, 1,
        facecolor='w',
        linewidth=0.,
        alpha=1)
    wbox.add_patch(rect)

    for p in range(1, 10):

        zmin_f = '{val: 1.{p}f}'.format(val=round(z_min, p), p=p)
        zmax_f = '{val: 1.{p}f}'.format(val=round(z_max, p), p=p)

        if np.abs(float(zmin_f) - float(zmax_f)) == 0:
            continue
            # increase precision (p+)
        else:
            xMTLl = r'$' + zmin_f + '$'
            xMTLr = r'$' + zmax_f + '$'
            break

    print('Ticks for:', vars_c[k])
    print(zmin_f, '<- ')
    print(zmax_f, '<- ')

    # Default colorbar dimensions
    cbbox_t = 0.05  # - top margin (wbox top margin is 0.0)
    cbbox_h = 0.455  # - colorbar box total height

    xMTLp = 0.035  # v and h pad before and after xMTL
    cblp = 0.05   # v and h pad before and after label

    # Colorbar label [does not actually render it]
    labeltext = plt.text(0., 0., vars_c[k])
    # Render colorbar label on canvas
    fig.canvas.draw()
    # Coordinates transformation from pixels to (x,y) in wbox
    transf = wbox.transAxes.inverted()
    # Get bbox object
    bboxo = labeltext.get_window_extent()
    # Make coordinates transformation
    bboxc = bboxo.transformed(transf)

    cblw = bboxc.x1 - bboxc.x0  # colorbar label width
    cblh = bboxc.y1 - bboxc.y0  # colorbar label height

    # remove this text
    labeltext.remove()
    # -----------------------------------

    # Left MTL label [does not actually render it]
    labeltext = plt.text(0., 0., xMTLl)
    fig.canvas.draw()
    transf = wbox.transAxes.inverted()
    bboxo = labeltext.get_window_extent()
    bboxc = bboxo.transformed(transf)

    xMTLlw = bboxc.x1 - bboxc.x0  # left x major tick width
    xMTLlh = bboxc.y1 - bboxc.y0  # left x major tick height

    labeltext.remove()
    # -----------------------------------

    # Right MTL label [does not actually render it]
    labeltext = plt.text(0., 0., xMTLr)
    fig.canvas.draw()
    transf = wbox.transAxes.inverted()
    bboxo = labeltext.get_window_extent()
    bboxc = bboxo.transformed(transf)

    xMTLrw = bboxc.x1 - bboxc.x0  # right x major tick width
    xMTLrh = bboxc.y1 - bboxc.y0  # right x major tick height

    labeltext.remove()
    # -----------------------------------

    # Place left xMTL
    labeltext = plt.text(xMTLp, xMTLp, xMTLl, transform=wbox.transAxes)

    # Place left edge of the colorbar in the third if the xMTLl
    cbbox_l = xMTLp + xMTLlw / 3  # <- more attractive
    # cbbox_l = xMTLp + xMTLlw/2 # <- less attractive

    # Colorbar label vertical position:
    cblvc = 1 - (cbbox_t + cbbox_h / 2 + cblh / 2)

    # Place colorbar text label
    labeltext = plt.text(1 - (cblp + cblw),
                         cblvc, vars_c[k],
                         transform=wbox.transAxes)

    # Color bar width
    cbbox_w = 1. - (cbbox_l + cblp + cblw + cblp)

    # Place right xMTL
    labeltext = plt.text(min(cbbox_l + cbbox_w - xMTLrw / 2 - xMTLp,
                             1. - (xMTLrw + xMTLp) + xMTLrw / 2),
                         xMTLp, xMTLr,
                         transform=wbox.transAxes)

    # Colorbar box [loc is fixed here]
    # bbox_to_anchor(x, y,1,1)+loc=2 -> place cbbox upper left corner in (x,y)
    cbbox = inset_axes(wbox,
                       str(cbbox_w * 100) + '%', str(cbbox_h * 100) + '%',
                       loc=2,
                       borderpad=0.0,
                       bbox_to_anchor=(cbbox_l, -cbbox_t, 1, 1),
                       bbox_transform=wbox.transAxes)
    rect = patches.Rectangle(
        (0, 0), 1, 1,
        facecolor='w',
        edgecolor='w',
        alpha=0)
    cbbox.add_patch(rect)

    # Colorbar
    fig.colorbar(cntr,
                 cax=cbbox,
                 orientation='horizontal',
                 ticks=[z_min, z_max],
                 extendfrac=0,
                 drawedges=False,
                 extendrect=True)

    # These 3 lines should remove default MTL
    cbbox.xaxis.set_major_formatter(plt.ScalarFormatter(useOffset=False))
    cbbox.ticklabel_format(axis='both', style='plain')
    cbbox.tick_params(labelbottom=False, labelcolor='r')
    # Add minor ticks
    cbbox.xaxis.set_minor_locator(AutoMinorLocator(n=int(z_levels - 1)))
    cbbox.tick_params(which='minor', length=8)
    cbbox.tick_params(which='major', length=12)

    # Show plot
    # plt.show()

    # Print to file ['tight' = no white space]
    file_pdf = saveto + vars_f[k] + '.pdf'
    file_png = saveto + vars_f[k] + '.png'
    plt.savefig(file_pdf,
                bbox_inches='tight',
                pad_inches=0)
    system('convert -density 300 ' + file_pdf + ' ' + file_png)

    # Finish
    plt.close()
