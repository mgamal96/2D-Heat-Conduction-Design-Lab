import numpy as np
from scipy.sparse.linalg import minres as solver

# Constants
hboard = 10 # for the board as well as the block without heat sink.
hsink = 12 # For the blocks with heat sink
t = 1.57
dx = 0.02 # since dx == dy
q = [1.032, 1.288, 0.975]
k = 8.73

# Initialize arrays
T = np.zeros(121)
A = np.zeros((121,121))
B = np.zeros(121)
heated = [[25,26,27,36,37,38,47,48,49] , [28,29,30,39,40,41,50,51,52], [70,71,72,81,82,83,92,93,94]]

# Boundary measurements
B[0:11] = [31.2, 32.8, 35.8, 40.5, 42.2, 41.6, 40.4, 38.4, 37.5, 34.2, 33.1]
B[110:] = [26.3, 27.1, 28.6, 30.2, 32.3, 33.5, 32.5, 30.8, 28.8, 27.5, 26.5]
B[0:111:11] = [31.2, 31.4, 32.2, 33.2, 33.2, 32.2, 30.6, 28.4, 28.6, 27.3, 26.3]
B[10:122 :11] = [32.1, 34.6, 37.2, 38.3, 37.6, 34.4, 32.6, 30.0, 28.3, 27.0, 26.5]


# Populate array with initial conditions from measurements
for i in range(0,10):
    A[i,i] = 1
for i in range(119,120):
    A[i,i] = 1
for i in range(0,119,11):
    A[i,i] = 1
for i in range(10,120,11):
    A[i,i] = 1

# Populate Array with Discretized Values
for i in range(10,119):
    if(i%11 == 0 or (i-1)%11==0):
        continue
    A[i//10, i%10-1] = (1/dx*dx)
    A[i//10, i%10+1] = (1/dx*dx)
    A[i//10 +1, i%10] = (1/dx*dx)
    A[i//10 -1, i%10] = (1/dx*dx)
    A[i//10, i%10] = -2*((1/dx*dx) + (1/dx*dx))

# Populate Heated Block conditions
for i, area in enumerate(heated):
    for node in area:
        B[node] = -q[i]/k

print(A.shape, B.shape)

# Solve for T array
T = solver(A, B)
print(T)
