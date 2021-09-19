# ----------------------------------------------------
# LES simulation [right] x, y [m], u,v,w [m/s], uu,vv,ww,uv,uw,vw [m^2/s^2]

D_r = 38.1 * 1e-3  # [m]
Ub_r = 18.7  # [m/s] Ub for try_11.5_0.32
Ub = Ub_r

dx_r = 0.003  # [-]
dy_r = 0.003  # [-]

# For 2d contourplots
x_min_r = 0.0  # [-]
x_max_r = 0.89  # [-]
y_min = -0.45  # [-] includes top of the swirler
y_max = 7.14  # [-]

# number of mesh nodes
n_grid_x_l = int((x_max_r - x_min_r) / dx_r) + 1
n_grid_y_l = int((y_max - y_min) / dy_r) + 1

# print('nx_r: ', n_grid_x_l)
# print('ny_r: ', n_grid_y_l)

# ----------------------------------------------------
# PIV experiment [left]  x, y [mm], u,v,w [m/s], uu,vv,ww,uv,uw,vw [m^2/s^2]

# x_l, dx_l, n_grid_x_l
# y_l, dy_l, n_grid_y_l
# are set in comb_data_2d_structured

x_min_l = -0.805  # [-]
x_max_l = 0.0  # [-]

# left:sim & sim
dx_l = 0.01  # [-]
dy_l = 0.01  # [-]

# number of mesh nodes
n_grid_x_r = int((x_max_l - x_min_l) / dx_l) + 1
n_grid_y_r = int((y_max - y_min) / dy_l) + 1

# --------------- -------------------------------------------------------------
# Axis settings
# --------------- -------------------------------------------------------------

xl_min_l = -0.5
xl_max_l = 0.0
xl_min_r = 0.0
xl_max_r = 0.5
yl_min = -1.0
yl_max = 1.0
dxl = 0.5
dyl = 0.5

# --------------- -------------------------------------------------------------
# Function settings
# --------------- -------------------------------------------------------------

R_1 = 12.7 * 1e-3 / D_r
R_2 = 17.4 * 1e-3 / D_r
C_4 = 0.02
C_5 = 0.02
C_1 = -1711.31 - 16.469 * C_4 - 126.881 * C_5
C_2 = 1351.93 + 19.5982 * C_4 + 134.519 * C_5
C_3 = -259.777 - 7.70422 * C_4 - 39.7568 * C_5
