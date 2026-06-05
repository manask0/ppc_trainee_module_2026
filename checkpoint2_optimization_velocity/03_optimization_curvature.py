import numpy as np
import matplotlib.pyplot as plt


def build_spline(x, y, L=0.0, R=0.0): # L = S"(x0), R = S"(xn)

    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    n = len(x) - 1
    h = np.zeros(n)

    for i in range(n):
        h[i] = x[i+1] - x[i]

    A = np.zeros((4*n, 4*n))
    rhs = np.zeros(4*n)

    row = 0

    # Position constraints
    for i in range(n):
        A[row, 4*i] = 1 # ai + bi*(x-xi)+ci*(x-xi)^2 + di*(x-xi)^3 
        rhs[row] = y[i]
        row += 1

        A[row, 4*i] = 1
        A[row, 4*i+1] = h[i]
        A[row, 4*i+2] = h[i]**2
        A[row, 4*i+3] = h[i]**3
        rhs[row] = y[i+1]
        row += 1

    # First derivative continuity
    # b_{i-1} + 2h_{i-1}c_{i-1} + 3h_{i-1}^2d_{i-1} - b_i=0
    for i in range(1, n):
        dx = h[i-1]

        A[row, 4*(i-1)+1] = 1
        A[row, 4*(i-1)+2] = 2*dx
        A[row, 4*(i-1)+3] = 3*dx**2

        A[row, 4*i+1] = -1
        row += 1

    # Second derivative continuity
    for i in range(1, n):
        dx = h[i-1]

        A[row, 4*(i-1)+2] = 2
        A[row, 4*(i-1)+3] = 6*dx

        A[row, 4*i+2] = -2
        row += 1

    # Boundary conditions (OPTIMIZABLE)
    A[row, 2] = 2
    rhs[row] = L
    row += 1

    A[row, 4*(n-1)+2] = 2
    A[row, 4*(n-1)+3] = 6*h[-1]
    rhs[row] = R
    row += 1

    coeffs = np.linalg.solve(A, rhs)

    # spline evaluator
    def S(xq):
        xq = np.array(xq, ndmin=1)
        yq = np.zeros_like(xq, dtype=float)

        for j, xv in enumerate(xq):
            i = np.searchsorted(x, xv) - 1
            i = max(0, min(i, n-1))

            dx = xv - x[i]

            a = coeffs[4*i]
            b = coeffs[4*i+1]
            c = coeffs[4*i+2]
            d = coeffs[4*i+3]

            yq[j] = a + b*dx + c*dx**2 + d*dx**3

        return yq if len(yq) > 1 else yq[0]

    return S



def curvature(xp, yp):
    dy = np.gradient(yp, xp)
    ddy = np.gradient(dy, xp)

    kappa = np.abs(ddy) / ((1 + dy**2)**1.5)

    return np.trapezoid(kappa, xp) 



def cost(L, R, x, y):

    Sy = build_spline(x, y, L, R)

    xp = np.linspace(x[0], x[-1], 200)
    yp = Sy(xp)

    return curvature(xp, yp)


def optimize(x, y, lr=2, steps=150):

    L = 0.0
    R = 0.0
    epsilon = 1e-4

    t = np.linspace(x[0], x[-1], 200)

    for i in range(steps):

        base = cost(L, R, x, y)

        grad = np.zeros(2)

        for j in range(2):
            th = [L, R].copy()
            th[j] += epsilon
            grad[j] = (cost(th[0], th[1], x, y) - base) / epsilon


        L -= lr * grad[0]
        R -= lr * grad[1]

        if i % 20 == 0:
            print(f"step {i}, cost = {base}")
    print(f"L : {L}, R : {R}")
    return [L,R]



if __name__ == "__main__":

    x = np.sort(np.random.choice(range(10), 4, replace=False))
    y = np.random.randint(0, 10, 4)

    print("x:", x)
    print("y:", y)

    t = np.linspace(x[0], x[-1], 200)

    # NATURAL SPLINE
    S_nat = build_spline(x, y, 0.0, 0.0)

    # OPTIMIZE
    L, R = optimize(x, y)

    S_opt = build_spline(x, y, L, R)

    # PLOT
    plt.figure()

    plt.plot(t, S_nat(t), label="Natural")
    plt.plot(t, S_opt(t), label="Optimized")

    plt.scatter(x, y)

    plt.legend()
    plt.show()