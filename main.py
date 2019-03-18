import numpy as np

# Constants
hboard = 10 # for the board as well as the block without heat sink.
hsink = 12 # For the blocks with heat sink
t = 1.57
dx = 0.02 # since dx == dy


# Initialize arrays
T = np.zeros((11*11))
A = np.zeros((11,11))

# Initial conditions from measurements
# --- put init conditions here --


# Populate Array
for i, temp in enumerate(T):
    A[i//10, i%10-1] = (1/dx*dx)
    A[i//10, i%10+1] = (1/dx*dx)
    A[i//10 +1, i%10] = (1/dx*dx)
    A[i//10 -1, i%10] = (1/dx*dx)
    A[i//10, i%10] = -2*((1/dx*dx) + (1/dx*dx))



# Solve for T array
T = np.linalg.solve(A, B)
