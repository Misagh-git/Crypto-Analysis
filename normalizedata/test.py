from matplotlib.pyplot import subplots
from numpy import linspace, random, sin, cos
from scipy import interpolate

x = linspace(0, 10)

y = sin(2*x * 1.5) + cos (x * 0.5)  + random.randn(x.size) * 1e-1
# fit spline
spl = interpolate.InterpolatedUnivariateSpline(x, y)
fitx = linspace(0, x.max(), 100)

fig, ax = subplots()
ax.scatter(x, y)

ax.plot(fitx, spl(fitx))
fig.show()