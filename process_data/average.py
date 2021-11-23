import numpy as np
import numpy.ma as ma
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from process_data.parameters import *


# Export csv from paraview:
# Save Data -> Point Data + Add Meta Data + Scientific Format


def download_data_from_pw(inp):
    x, y, z, u, v, w, uu, vv, ww, uv, vw, uw \
        = np.loadtxt(inp,
                     usecols=(0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14),
                     delimiter=',',
                     skiprows=1,
                     unpack=True)
    x = x / D_r
    y = y / D_r
    z = z / D_r

    u = u / Ub_r
    v = v / Ub_r
    w = w / Ub_r

    uu = uu / Ub_r ** 2
    vv = vv / Ub_r ** 2
    ww = ww / Ub_r ** 2
    uv = uv / Ub_r ** 2
    uw = uw / Ub_r ** 2
    vw = vw / Ub_r ** 2
    return x, y, z, u, v, w, uu, vv, ww, uv, vw, uw


def count_averages(x, y, z, u, v, w, uu, vv, ww, uv, vw, uw):
    # rotation axis
    x0 = 0
    y0 = 0

    print("x0:", x0)
    print("y0:", y0)

    # --------------- -------------------------------------------------------------
    # Circumferential angle
    # --------------- -------------------------------------------------------------

    # theta [0; 2pi]
    theta = np.arctan2(y, x)
    c = np.cos(theta)
    s = np.sin(theta)

    # --------------- -------------------------------------------------------------
    # Averaging over angle simulation [right plot]
    # --------------- -------------------------------------------------------------

    r = np.sqrt(x ** 2 + y ** 2)

    uu_mean = uu + u * u  # <ux * ux> = <u'x * u'x> + <ux> * <ux>
    vv_mean = vv + v * v  # <uy * uy> = <u'y * u'y> + <uy> * <uy>
    uv_mean = uv + u * v  # <ux * uy> = <u'x * u'y> + <ux> * <uy>
    uw_mean = uw + u * w  # <ux * uz> = <u'x * u'z> + <ux> * <uz>
    vw_mean = vw + v * w  # <uy * uz> = <u'y * u'z> + <uy> * <uz>

    urur_mean = \
        uu_mean * c ** 2. + vv_mean * s ** 2. + 2. * uv_mean * c * s  # <ur * ur>
    upup_mean = \
        uu_mean * s ** 2. + vv_mean * c ** 2. - 2. * uv_mean * c * s  # <uphi * uphi>
    urup_mean = - uu_mean * c * s + uv_mean * (c ** 2. - s ** 2) + \
                vv_mean * c * s  # <ur * uphi>
    uruz_mean = uw_mean * c + vw_mean * s  # <ur * uy>
    upuz_mean = - uw_mean * s + vw_mean * c  # <up * uy>

    ur = u * c + v * s  # <ur>
    up = - u * s + v * c  # <uphi>

    urur = urur_mean - ur * ur  # <u'r * u'r>
    upup = upup_mean - up * up  # <u'phi * u'phi>
    uruz = uruz_mean - ur * w  # <u'r * u'z>
    urup = urup_mean - ur * up  # <u'r * u'phi>
    upuz = upuz_mean - up * w  # <u'z * u'phi>

    # ----------------------------------------------------------------------------
    # Create bins for statistics
    # ----------------------------------------------------------------------------

    ''' Looks horrible for cubic, but ok for nearest: '''

    # Xi = np.linspace(x_min_r, x_max_r, n_grid_x_r)
    # Yi = np.linspace(y_min, y_max, n_grid_y_r)

    ''' Looks better for cubic: '''

    Xi = np.linspace(x_min_r - dx_r / 2, x_max_r + dx_r / 2, n_grid_x_r + 1)
    Yi = np.linspace(y_min - dy_r / 2, y_max + dy_r / 2, n_grid_y_r + 1)

    r_avg = stats.binned_statistic_2d(r, z, r, 'mean', bins=[Xi, Yi])
    z_avg = stats.binned_statistic_2d(r, z, z, 'mean', bins=[Xi, Yi])
    theta_avg = stats.binned_statistic_2d(r, z, theta, 'mean', bins=[Xi, Yi])
    ur_avg = stats.binned_statistic_2d(r, z, ur, 'mean', bins=[Xi, Yi])
    up_avg = stats.binned_statistic_2d(r, z, up, 'mean', bins=[Xi, Yi])
    w_avg = stats.binned_statistic_2d(r, z, w, 'mean', bins=[Xi, Yi])
    urur_avg = stats.binned_statistic_2d(r, z, urur, 'mean', bins=[Xi, Yi])
    ww_avg = stats.binned_statistic_2d(r, z, ww, 'mean', bins=[Xi, Yi])
    upup_avg = stats.binned_statistic_2d(r, z, upup, 'mean', bins=[Xi, Yi])
    uruz_avg = stats.binned_statistic_2d(r, z, uruz, 'mean', bins=[Xi, Yi])
    urup_avg = stats.binned_statistic_2d(r, z, urup, 'mean', bins=[Xi, Yi])
    upuz_avg = stats.binned_statistic_2d(r, z, upuz, 'mean', bins=[Xi, Yi])

    r = ma.masked_invalid(r_avg.statistic)
    z = ma.masked_invalid(z_avg.statistic)
    theta = ma.masked_invalid(theta_avg.statistic)
    ur = ma.masked_invalid(ur_avg.statistic)
    w = ma.masked_invalid(w_avg.statistic)
    up = ma.masked_invalid(up_avg.statistic)
    urur = ma.masked_invalid(urur_avg.statistic)
    ww = ma.masked_invalid(ww_avg.statistic)
    upup = ma.masked_invalid(upup_avg.statistic)
    uruz = ma.masked_invalid(uruz_avg.statistic)
    urup = ma.masked_invalid(urup_avg.statistic)
    upuz = ma.masked_invalid(upuz_avg.statistic)

    # remove masked [always 1D array]
    r = r.compressed()
    z = z.compressed()
    theta = theta.compressed()
    ur = ur.compressed()
    up = up.compressed()
    w = w.compressed()
    urur = urur.compressed()
    upup = upup.compressed()
    ww = ww.compressed()
    uruz = uruz.compressed()
    urup = urup.compressed()
    upuz = upuz.compressed()

    # x = -r  # used for left:sim & sim
    x = r
    z = z
    y = theta
    u = ur
    v = up
    w = w
    uu = urur
    vv = upup
    ww = ww
    uv = urup
    uw = uruz
    vw = upuz
    # --------------- -------------------------------------------------------------
    # Interpolation of unstructured data on structured grid [right plot]
    # --------------- -------------------------------------------------------------
    # Create structured grid
    Xi = np.linspace(x_min_r, x_max_r, n_grid_x_r)
    # Xi = np.linspace(x_min_l, x_max_l, n_grid_x_r)  # used for left:sim & sim
    Yi = np.linspace(y_min, y_max, n_grid_y_r)
    x_i, z_i = np.meshgrid(Xi, Yi)

    # --------------- -------------------------------------------------------------
    # Data interpolation [old method]
    # --------------- -------------------------------------------------------------
    # # create triangulated mesh
    # tri_mesh = tri.Triangulation(x, y)
    #
    # # mask triangles with zero area
    # xy = np.dstack((tri_mesh.x[tri_mesh.triangles],
    #                 tri_mesh.y[tri_mesh.triangles]))  # shape (ntri,3,2)
    # twice_area = np.cross(xy[:, 1, :] - xy[:, 0, :],
    #                       xy[:, 2, :] - xy[:, 0, :])  # shape (ntri)
    # mask = (twice_area < 1e-10)  # shape (ntri)
    # if np.any(mask):
    #     tri_mesh.set_mask(mask)
    #
    # # create triangulation function
    # z_tri = tri.CubicTriInterpolator(tri_mesh, z, kind='geom')
    # u_tri = tri.CubicTriInterpolator(tri_mesh, u, kind='geom')
    # v_tri = tri.CubicTriInterpolator(tri_mesh, v, kind='geom')
    # w_tri = tri.CubicTriInterpolator(tri_mesh, w, kind='geom')
    # c1_tri = tri.CubicTriInterpolator(tri_mesh, c1, kind='geom')
    # uu_tri = tri.CubicTriInterpolator(tri_mesh, uu, kind='geom')
    # vv_tri = tri.CubicTriInterpolator(tri_mesh, vv, kind='geom')
    # ww_tri = tri.CubicTriInterpolator(tri_mesh, ww, kind='geom')
    # uv_tri = tri.CubicTriInterpolator(tri_mesh, uv, kind='geom')
    # uw_tri = tri.CubicTriInterpolator(tri_mesh, uw, kind='geom')
    # vw_tri = tri.CubicTriInterpolator(tri_mesh, vw, kind='geom')
    #
    # # interpolate triangulated values on structured mesh
    # # Warning: u_i, v_i, .. have masked values
    # z_i = z_tri(x_i, y_i)
    # u_i = u_tri(x_i, y_i)
    # v_i = v_tri(x_i, y_i)
    # w_i = w_tri(x_i, y_i)
    # c1_i = c1_tri(x_i, y_i)
    # uu_i = uu_tri(x_i, y_i)
    # vv_i = vv_tri(x_i, y_i)
    # ww_i = ww_tri(x_i, y_i)
    # uv_i = uv_tri(x_i, y_i)
    # uw_i = uw_tri(x_i, y_i)
    # vw_i = vw_tri(x_i, y_i)

    # --------------- -------------------------------------------------------------
    # Data interpolation [new method]
    # --------------- -------------------------------------------------------------

    y_i = griddata(np.transpose([x, z]), y, (x_i, z_i), method="nearest")
    u_i = griddata(np.transpose([x, z]), u, (x_i, z_i), method="nearest")
    v_i = griddata(np.transpose([x, z]), v, (x_i, z_i), method="nearest")
    w_i = griddata(np.transpose([x, z]), w, (x_i, z_i), method="nearest")
    uu_i = griddata(np.transpose([x, z]), uu, (x_i, z_i), method="nearest")
    vv_i = griddata(np.transpose([x, z]), vv, (x_i, z_i), method="nearest")
    ww_i = griddata(np.transpose([x, z]), ww, (x_i, z_i), method="nearest")
    uv_i = griddata(np.transpose([x, z]), uv, (x_i, z_i), method="nearest")
    uw_i = griddata(np.transpose([x, z]), uw, (x_i, z_i), method="nearest")
    vw_i = griddata(np.transpose([x, z]), vw, (x_i, z_i), method="nearest")

    # --------------- -------------------------------------------------------------
    # Export output_file(s)
    # --------------- -------------------------------------------------------------

    array_to_export = np.array([np.ravel(x_i),
                                np.ravel(y_i),
                                np.ravel(z_i),
                                np.ravel(u_i),
                                np.ravel(v_i),
                                np.ravel(w_i),
                                np.ravel(uu_i),
                                np.ravel(vv_i),
                                np.ravel(ww_i),
                                np.ravel(uv_i),
                                np.ravel(uw_i),
                                np.ravel(vw_i)
                                ]).T
    x_r = np.reshape(x_i, (n_grid_y_r, n_grid_x_r))
    z_r = np.reshape(z_i, (n_grid_y_r, n_grid_x_r))
    u_r = np.reshape(w_i, (n_grid_y_r, n_grid_x_r))

    fig, ax = plt.subplots(1, 1, figsize=[1000. / 300, 8000. / 300])

    # Tune subplot layout, hspace for h interval
    plt.subplots_adjust(left=0.12, bottom=0.12, wspace=0.)
    # -------------------------------------------------------
    cntr = ax.contourf(x_r, z_r, u_r,
                       levels=30,
                       extend='both')
    plt.show()
    return array_to_export, u_i


def save(inp_f, tup):
    array_to_export = tup[0]
    u_i = tup[1]
    out_file = inp_f.replace('.csv', '') + '_average_data_to_2d_matplotlib' + '.tsv'
    np.savetxt(out_file, array_to_export, fmt='% .8e',
               delimiter='\t',
               header='nx: ' + str(np.shape(u_i)[0]) + ' '
                                                       'ny: ' + str(np.shape(u_i)[1]) + ' '
                                                                                        '0:x 1:<y> 2:z 3:<u_r> '
                                                                                        '4:<u_phi> 5:<u_z> \ 6:<u_r '
                                                                                        'u_r> 7:<u_phi u_phi> 8:<u_z '
                                                                                        'u_z> \ 9:<u_r u_phi> 10:<u_r '
                                                                                        'u_z> 11:<u_phi u_z> '
               )
    return out_file
