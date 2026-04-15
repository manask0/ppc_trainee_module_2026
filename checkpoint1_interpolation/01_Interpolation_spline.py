import numpy as np
import matplotlib.pyplot as plt

x = x = np.sort(np.random.choice(range(10), size=4, replace=False)) # [x0, x1, x2, x3]
y = np.random.randint(0, 10, size=4) # [y0, y1, y2, y3]
h = np.zeros(3)
for i in range (3):
    h[i] = x[i+1]-x[i]


t = np.zeros(12) 
A = np.zeros((12, 12)) #12 eqns 12 unknowns [0 a0 1 b0 2 c0 3 d0 4 a1 5 b1 6 c1 7 d1 8 a2 9 b2 10 c2 11 d2]
row = 0

for i in range (3):
    A[row, 4*i] = 1
    t[row] = y[i]
    row +=1
    A[row, 4*i] = 1
    A[row, 4*i+1] = h[i]
    A[row, 4*i+2] = h[i]**2
    A[row, 4*i+3] = h[i]**3
    t[row] = y[i+1]
    row+=1

for i in range(1, 3):
    # b_{i-1} + 2c_{i-1}dx + 3d_{i-1}dx^2 - b_i = 0
    dx = h[i-1]
    A[row, 4*(i-1) + 1] = 1
    A[row, 4*(i-1) + 2] = 2*dx
    A[row, 4*(i-1) + 3] = 3*dx**2
    A[row, 4*i + 1] = -1
    row += 1

for i in range(1, 3):
    dx = h[i-1]

    # 2c_{i-1} + 6d_{i-1}dx - 2c_i = 0
    A[row, 4*(i-1) + 2] = 2
    A[row, 4*(i-1) + 3] = 6*dx

    A[row, 4*i + 2] = -2
    row += 1

# Natural boundary conditions
A[row, 2] = 2
row += 1
A[row, 10] = 2
A[row, 11] = 6*h[2]
row += 1

# Solving system of eqns
coeffs = np.linalg.solve(A, t)

def spline(i, xi):
    a = coeffs[4*i]
    b_ = coeffs[4*i + 1]
    c = coeffs[4*i + 2]
    d = coeffs[4*i + 3]

    dx = xi - x[i]   
    return a + b_*dx + c*dx**2 + d*dx**3

X, Y = [], []

for i in range(3):
  xi = np.linspace(x[i], x[i+1], 50)
  yi = spline(i, xi)
  X.extend(xi)
  Y.extend(yi)


plt.plot(X,Y,label="Spline Interpolation")
plt.scatter(x, y)
plt.show()






