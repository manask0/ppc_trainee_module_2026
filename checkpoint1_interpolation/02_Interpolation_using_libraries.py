import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import interpolate

df = pd.read_csv('loop_track_waypoints.csv')

x = df['X'].to_numpy()
y = df['Y'].to_numpy()
# Problem : We can't interpolate based on increasing x, since we need a closed loop based on order of cones.
# For this, we need to represent the data points in terms of a parameter u which constnatly increases. x = x(u) and y = y(u)
# u can be thought of as distance along curve, in the range [0, 1)
tck, u = scipy.interpolate.splprep([x, y], s=0)
#tck stores spline representation, u is the hidden parameter.
#s = 0. says that spline must pass through all points. s is smoothening factor, if s>0 then smoothening is given priority and curve may not pass through all points.
#tck = tuple of t, c, k where t->knots, c-> coeffecients, k-> degree

unew = np.arange(0, 1.00, 0.005)
# generating many steps between 0 and 1 to densely sample the curve.
out = scipy.interpolate.splev(unew, tck)
# out[0] gives x values, out[1] gives y values.




xi, yi = out
fig, ax = plt.subplots(1, 1)
ax.plot(x, y, 'or') #circle markers, red colour
ax.plot(xi, yi, '-b') #solid line, blue colour




plt.show()
