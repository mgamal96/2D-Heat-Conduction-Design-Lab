import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class board(object):
    """ Circuit board heat transfer simulator. Numerical solution to Heat-Diffusion PDE """

    def __init__(self, rows, cols, dx, thickness, Tinf, k, bcs, components):
        """
        Args:
            rows: (int) number of nodes along height
            cols: (int) number of nodes along width
            l: distance between two nodes in Meters
            h: convective heat trasfer coefficient
            k: conductive heat transfer coefficient of board material
            bcs: (python dict)
            components: (np.array) components dims and heat generation [x1, y1, x2, y2, e]. Shape: [K, 5]
        """
        self.rows = rows
        self.cols = cols
        self.dx = dx
        self.t = thickness
        self.Taa = 64
        self.k = k
        self.Tinf = Tinf
        # self.h = h
        self.N = self.rows * self.cols
        self.bcs = bcs
        self.components = components

        self.heatedMask, self.eGenMask = self.getMasks(self.components)
        self.heatedNodes = np.copy(self.heatedMask).flatten()
        self.eGenNodes = np.copy(self.eGenMask).flatten()

    def getMasks(self, components):
        """
        Args:
            components: (np.array) components dims [x1, y1, x2, y2, e] Shape: [K, 5]
            components: (np.array) components dims [row, col e] Shape: [K, 3]
        Returns:
            heatedMask: (np.array) integer mask indicating egen at node (0 for none.) Shape: [rows, cols]
            eGenMask: (np.array) e generation mask indicating the generation at a node, Shape: [rows, cols]
        """

        heatedMask = np.zeros((self.rows, self.cols))
        eGenMask = np.zeros((self.rows, self.cols))

        for i in range(len(components)):
            row, col, e = components[i]
            row, col = int(row), int(col)

            # Egen in area
            eGenMask[row-1: row+2, col-1:col+2] = e

            # Ratio of node area involving generation
            heatedMask[row-1:row+2,col], heatedMask[row,col-1:col+2] = 0.5, 0.5
            heatedMask[row-1,col-1], heatedMask[row-1, col+1] = 0.25, 0.25
            heatedMask[row+1,col-1], heatedMask[row+1, col+1] = 0.25, 0.25
            heatedMask[row, col] = 1



        return heatedMask, eGenMask

    def idx2coord(self, i):
        """ Converts index to (row, col)
        """

        row = i // self.cols
        col = i % self.cols

        return np.array([row, col])

    def solve(self):
        """ Builds and Solves linear system of equations
        Returns:
            T: (np.array) temperatures array, Shape: [Rows, Cols]
        """

        # Set up Array
        A = np.zeros((self.N, self.N))
        B = np.zeros((self.N, 1))


        for i in range(self.cols, self.N - self.cols ):


            R = self.heatedNodes[i]        # ratio of covered by heated components
            A[i, i] = -4.0
            A[i, i - self.cols] = 1.0
            A[i, i + self.cols] = 1.0
            A[i, i - 1 ] =  1.0
            A[i, i + 1 ] = 1.0

            e = self.eGenNodes[i]
            B[i] = - R * (e * self.dx * self.dx /self.k)


        # Boundary conditons
        for key in self.bcs:
            A[key, :] = 0.0
            A[key, key] = 1.0
            B[key] = self.bcs[key]


        # Solve for Temps
        Ainv = np.linalg.inv(A)
        T = np.matmul(Ainv, B)

        plt.figure(figsize = (1,2))
        gs1 = gridspec.GridSpec(1, 2)
        gs1.update(wspace=0.025, hspace=0.05) # set the spacing between axes.

        ax1 = plt.subplot(gs1[0])
        plt.title('Heat Contour Map')
        plt.contourf(T .reshape(11,11) - 273, origin='upper'); plt.colorbar();
        ax1.set_aspect('equal')


        ax2 = plt.subplot(gs1[1])
        plt.title('Circuit Board')
        hh = np.copy(self.heatedMask)
        hh[hh > 0] = 1
        board = np.zeros((11,11,3), dtype=np.uint8) + np.array([[[0,255,0]]])
        board[hh == 1] = np.array([0,0,0])
        board = board.astype(np.uint8)
        plt.imshow(board, interpolation='nearest')
        ax2.set_aspect('equal')
        plt.show()


        return T
