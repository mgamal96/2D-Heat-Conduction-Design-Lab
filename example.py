import numpy as np
from board import *

# Circuit board parameters
rows, cols = 51, 51
dx = 0.02
k = 401 # copper
egens = [4500000/2, 4500000/2, 4500000/2]
thickness = 1.57/1000
Tinf = 295.5

# Circuit Board Components
# components = np.array([[2,2, egens[0]], [6,2, egens[1]], [6,6, egens[1]] ])
components = np.array([
[23,23, egens[1]], [27,27, egens[1]], [23,27, egens[1]], [27,23, egens[1]],
[23,35, egens[1]], [23,37, egens[1]], [23,39, egens[1]],
[28,39, egens[1]], [31,39, egens[1]], [33,39, egens[1]], [36,39, egens[1]],
[12,12, egens[1]], [13,13, egens[1]], [12,13, egens[1]], [13,12, egens[1]],
[12,17, egens[1]], [12,19, egens[1]], [12,22, egens[1]], [12,25, egens[1]],
[40,10, egens[1]], [44,14, egens[1]], [44,10, egens[1]], [40,14, egens[1]],
])



# Populate Boundary Condiditons
bcs = {}
# top = [31.2, 32.8, 35.8, 40.5, 42.2, 41.6, 40.4, 39.4, 37.5, 34.2, 32.1]
# bottom = [26.3, 27.1, 28.6, 30.2, 32.3, 33.5, 32.5, 30.8, 28.8, 27.5, 26.5]
# left = [31.2, 31.4, 32.2, 33.2, 33.2, 32.2, 30.6, 28.4, 28.6, 27.3, 26.3]
# right = [32.1, 34.6, 37.2, 38.3, 37.6, 34.4, 32.6, 30.0, 28.3, 27.0, 26.5]

# top = [40.5]*cols
# bottom = [33.5]*cols
# left = [32.2]*cols
# right = [37]*cols

top = [25]*cols
bottom = [31]*cols
left = [25]*cols
right = [31]*cols


k1, k2, k3 = 0, 0, 0
# for i in range(0,11):
for i in range(0,cols):
    bcs[i] = top[i]  + 273
# for i in range(110, 121):
for i in range(rows*cols - cols, rows*cols):
    bcs[i] = bottom[k1]  + 273
    k1 +=1
for i in range(0, rows*cols - cols + 1, cols):
# for i in range(0, 111, 11):
    bcs[i] = left[k2] + 273
    k2+=1
# for i in range(10, 122, 11):
for i in range(cols-1, rows*cols + 1, cols):
    bcs[i] = right[k3] + 273
    k3+=1


# Instatiate board and solve
brd = board(rows, cols, dx, thickness, Tinf, k, bcs, components)
T = brd.solve()
plt.contourf(T .reshape(rows,cols) - 273, origin='upper'); plt.colorbar(); plt.show()
