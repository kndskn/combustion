import numpy as np
import numpy.ma as ma
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from parameters import *

# Export csv from paraview:
# Save Data -> Point Data + Add Meta Data + Scientific Format


def download_data_from_pw(inp):
    x, z, y, u, w, v, uu, uw, uv, ww, vw, vv \
        = np.loadtxt(inp,
                     usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
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
    return x, z, y, u, w, v, uu, uw, uv, ww, vw, vv


def count_averages(x, z, y, u, w, v, uu, uw, uv, ww, vw, vv):
    # rotation axis
    x0 = 0
    z0 = 0

    print("x0:", x0)
    print("z0:", z0)

    # x = x - x0
    # z = z - z0

    # --------------- -------------------------------------------------------------
    # Circumferential angle
    # --------------- -------------------------------------------------------------

    # theta [0; 2pi]
    theta = np.arctan2(z, x)
    c = np.cos(theta)
    s = np.sin(theta)

    # --------------- -------------------------------------------------------------
    # Averaging over angle simulation [right plot]
    # --------------- -------------------------------------------------------------

    # rotation matrix (or you can use x = np.sqrt(x**2 + z**2) - same result)
    # x = x * c + z * s
    # z = - x * s + z * c
    r = np.sqrt(x ** 2 + z ** 2)

    uu_mean = uu + u * u  # <ux * ux> = <u'x * u'x> + <ux> * <ux>
    ww_mean = ww + w * w  # <uz * uz> = <u'z * u'z> + <uz> * <uz>
    uv_mean = uv + u * v  # <ux * uy> = <u'x * u'y> + <ux> * <uy>
    uw_mean = uw + u * w  # <ux * uz> = <u'x * u'z> + <ux> * <uz>
    vw_mean = vw + v * w  # <uy * uz> = <u'y * u'z> + <uy> * <uz>

    urur_mean = \
        uu_mean * c ** 2. + ww_mean * s ** 2. + 2. * uw_mean * c * s  # <ur * ur>
    upup_mean = \
        uu_mean * s ** 2. + ww_mean * c ** 2. - 2. * uw_mean * c * s  # <uphi * uphi>
    urup_mean = - uu_mean * c * s + uw_mean * (c ** 2. - s ** 2) + \
                ww_mean * c * s  # <ur * uphi>
    uruy_mean = uv_mean * c + vw_mean * s  # <ur * uy>
    upuy_mean = - uv_mean * s + vw_mean * c  # <up * uy>

    ur = u * c + w * s  # <ur>
    up = - u * s + w * c  # <uphi>

    urur = urur_mean - ur * ur  # <u'r * u'r>
    upup = upup_mean - up * up  # <u'phi * u'phi>
    uruy = uruy_mean - ur * v  # <u'r * u'y>
    urup = urup_mean - ur * up  # <u'r * u'phi>
    upuy = upuy_mean - up * v  # <u'y * u'phi>

    # ----------------------------------------------------------------------------
    # Create bins for statistics
    # ----------------------------------------------------------------------------

    ''' Looks horrible for cubic, but ok for nearest: '''

    # Xi = np.linspace(x_min_r, x_max_r, n_grid_x_r)
    # Yi = np.linspace(y_min, y_max, n_grid_y_r)

    ''' Looks better for cubic: '''

    Xi = np.linspace(x_min_r - dx_r / 2, x_max_r + dx_r / 2, n_grid_x_r + 1)
    Yi = np.linspace(y_min - dy_r / 2, y_max + dy_r / 2, n_grid_y_r + 1)

    r_avg = stats.binned_statistic_2d(r, y, r, 'mean', bins=[Xi, Yi])
    y_avg = stats.binned_statistic_2d(r, y, y, 'mean', bins=[Xi, Yi])
    theta_avg = stats.binned_statistic_2d(r, y, theta, 'mean', bins=[Xi, Yi])
    ur_avg = stats.binned_statistic_2d(r, y, ur, 'mean', bins=[Xi, Yi])
    v_avg = stats.binned_statistic_2d(r, y, v, 'mean', bins=[Xi, Yi])
    up_avg = stats.binned_statistic_2d(r, y, up, 'mean', bins=[Xi, Yi])
    urur_avg = stats.binned_statistic_2d(r, y, urur, 'mean', bins=[Xi, Yi])
    vv_avg = stats.binned_statistic_2d(r, y, vv, 'mean', bins=[Xi, Yi])
    upup_avg = stats.binned_statistic_2d(r, y, upup, 'mean', bins=[Xi, Yi])
    uruy_avg = stats.binned_statistic_2d(r, y, uruy, 'mean', bins=[Xi, Yi])
    urup_avg = stats.binned_statistic_2d(r, y, urup, 'mean', bins=[Xi, Yi])
    upuy_avg = stats.binned_statistic_2d(r, y, upuy, 'mean', bins=[Xi, Yi])

    r = ma.masked_invalid(r_avg.statistic)
    y = ma.masked_invalid(y_avg.statistic)
    theta = ma.masked_invalid(theta_avg.statistic)
    ur = ma.masked_invalid(ur_avg.statistic)
    v = ma.masked_invalid(v_avg.statistic)
    up = ma.masked_invalid(up_avg.statistic)
    urur = ma.masked_invalid(urur_avg.statistic)
    vv = ma.masked_invalid(vv_avg.statistic)
    upup = ma.masked_invalid(upup_avg.statistic)
    uruy = ma.masked_invalid(uruy_avg.statistic)
    urup = ma.masked_invalid(urup_avg.statistic)
    upuy = ma.masked_invalid(upuy_avg.statistic)

    # remove masked [always 1D array]
    r = r.compressed()
    y = y.compressed()
    theta = theta.compressed()
    ur = ur.compressed()
    v = v.compressed()
    up = up.compressed()
    urur = urur.compressed()
    vv = vv.compressed()
    upup = upup.compressed()
    uruy = uruy.compressed()
    urup = urup.compressed()
    upuy = upuy.compressed()

    # x = -r  # used for left:sim & sim
    x = r
    y = y
    z = theta
    u = ur
    v = v
    w = up
    uu = urur
    vv = vv
    ww = upup
    uv = uruy
    uw = urup
    vw = upuy
    # --------------- -------------------------------------------------------------
    # Interpolation of unstructured data on structured grid [right plot]
    # --------------- -------------------------------------------------------------
    # Create structured grid
    Xi = np.linspace(x_min_r, x_max_r, n_grid_x_r)
    # Xi = np.linspace(x_min_l, x_max_l, n_grid_x_r)  # used for left:sim & sim
    Yi = np.linspace(y_min, y_max, n_grid_y_r)
    x_i, y_i = np.meshgrid(Xi, Yi)

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

    z_i = griddata(np.transpose([x, y]), z, (x_i, y_i), method="nearest")
    u_i = griddata(np.transpose([x, y]), u, (x_i, y_i), method="nearest")
    v_i = griddata(np.transpose([x, y]), v, (x_i, y_i), method="nearest")
    w_i = griddata(np.transpose([x, y]), w, (x_i, y_i), method="nearest")
    uu_i = griddata(np.transpose([x, y]), uu, (x_i, y_i), method="nearest")
    vv_i = griddata(np.transpose([x, y]), vv, (x_i, y_i), method="nearest")
    ww_i = griddata(np.transpose([x, y]), ww, (x_i, y_i), method="nearest")
    uv_i = griddata(np.transpose([x, y]), uv, (x_i, y_i), method="nearest")
    uw_i = griddata(np.transpose([x, y]), uw, (x_i, y_i), method="nearest")
    vw_i = griddata(np.transpose([x, y]), vw, (x_i, y_i), method="nearest")

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
    y_r = np.reshape(y_i, (n_grid_y_r, n_grid_x_r))
    u_r = np.reshape(w_i, (n_grid_y_r, n_grid_x_r))

    fig, ax = plt.subplots(1, 1, figsize=[1000. / 300, 8000. / 300])

    # Tune subplot layout, hspace for h interval
    plt.subplots_adjust(left=0.12, bottom=0.12, wspace=0.)
    # -------------------------------------------------------
    cntr = ax.contourf(x_r, y_r, u_r,
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
                                                                                        '0:x 1:y 2:<z> 3:<u_r> 4:<u_x> 5:<u_phi> \
                                                                                         6:<u_r u_r> 7:<u_x u_x> 8:<u_phi u_phi> \
                                                                                         9:<u_r u_x> 10:<u_r u_phi> 11:<u_x u_phi>'
               )
    return out_file
