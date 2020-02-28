import numpy as np
from board import *

# Circuit board parameters
rows, cols = 11, 11
dx = 0.02
k = 401 # copper
egens = [45000000/2, 45000000/2, 45000000/2]
thickness = 1.57/1000
Tinf = 295.5

# Circuit Board Components
components = np.array([[2,2, egens[0]], [6,2, egens[1]], [6,6, egens[1]] ])

# Populate Boundary Condiditons
bcs = {}
top = [31.2, 32.8, 35.8, 40.5, 42.2, 41.6, 40.4, 39.4, 37.5, 34.2, 32.1]
bottom = [26.3, 27.1, 28.6, 30.2, 32.3, 33.5, 32.5, 30.8, 28.8, 27.5, 26.5]
left = [31.2, 31.4, 32.2, 33.2, 33.2, 32.2, 30.6, 28.4, 28.6, 27.3, 26.3]
right = [32.1, 34.6, 37.2, 38.3, 37.6, 34.4, 32.6, 30.0, 28.3, 27.0, 26.5]

k1, k2, k3 = 0, 0, 0

for i in range(0,11):
    bcs[i] = top[i]  + 273
for i in range(110, 121):
    bcs[i] = bottom[k1]  + 273
    k1 +=1
for i in range(0, 111, 11):
    bcs[i] = left[k2] + 273
    k2+=1
for i in range(10, 122, 11):
    bcs[i] = right[k3] + 273
    k3+=1


# Instatiate board and solve
brd = board(rows, cols, dx, thickness, Tinf, k, bcs, components)
T = brd.solve()
plt.contourf(T .reshape(11,11) - 273, origin='upper'); plt.colorbar(); plt.show()
