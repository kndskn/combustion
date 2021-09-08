# file: comb_data_3d_unstructured
import numpy as np
from plot_parameters import *

# Export csv from paraview:
# Save Data -> Point Data + Add Meta Data + Scientific Format

input_file = 'from_paraview_turbulent.csv'
x, z, y, u, w, v, uu, ww, vv, uw, uv, vw \
    = np.loadtxt(input_file,
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

uu = uu / Ub_r**2
vv = vv / Ub_r**2
ww = ww / Ub_r**2
uv = uv / Ub_r**2
uw = uw / Ub_r**2
vw = vw / Ub_r**2
