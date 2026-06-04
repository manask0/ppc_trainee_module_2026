Progress Tracker 
- [x] Cubic Interpolation Without Libraries
- [x] Interpolation using scipy libraries
- [ ] Linear Interpolation of Task - 02






Git Workflow for using forked repos : 
1) git clone https://github.com/manask0/ppc_trainee_module_2026
2) cd ppc_trainee_module_2026
3) git remote add upstream https://github.com/ppc_trainee_module_2026.git
4) git checkout -b CheckPoint1_Soln
5) Edit files
6) git add .
   git commit -m "message"
   git push


----------------------
We choose interpolation instead of choosing a sinlge polynomial n (one lesser than number of points) to avoid rapid oscillations. 

---------------------

### Linear Spline Interpolation
$$
f_1(x) = Y_i + \frac{Y_{i+1}-Y_i}{X_{i+1}-X_i}(x-X_i), \;\mid\;

X_i<=x<=X_{i+1}

$$
Drawbacks
1) Interior Knot : An interior data point which is a knot, ie shared by two data points.
2) In linear spline interpolation, derivative changes at interior knots. 
	Linear Spline Interpolation doesn't use data from points outside the two points when we try to predict value of an unknown x, since we only use data provided by $X_i$ and $X_{i+1}$ between which x lies.
------------------------
### Quadratic Spline Interpolation
Through two consecutive data points, we fit a quadratic. Say we have n+1 data points, from $X_0, Y_0$ to $X_n, Y_n.$ Then, between each pair of consecutive data points, we fit a spline of the form $a_ix^2 + b_ix + c_i$, giving us n splines with a total of 3n unknowns. We now need 3n simultaneous linear equations. How?
1) Each spline goes through two data points. This gives us 2n equations. 
2) Consecutive splines have same slopes at the interior knots. There are n+1 knots, but we don't get an equation at the first and last data points since these only have one spline each. So, the slope condition gives us n-1 equations. 
3) Assume $a_1$ = 0, ie saying that the first spline is linear and not quadratic.

--------------------------
### Cubic Spline Interpolation
Let S(x) be a cubic polynomial denoted by $S_i(x)$ on \[$x_i, x_{i+1}$] 
Then, we need 4n equations. 2n come from 2 data points per spline. n-1 come from equating first derivatives at n-1 interior knots. n-1 come from equating second derivatives at interior knots. For the two additional required equations, we either equate second derivatives at both end ponts to 0 (this is called natural/ free boundary) or equate slope of first and last splines at first and last data points to the corresponding slopes of the function whose values at nodes (the n+1 points) are taken to generate the n+1 data points (this is called clamped boundary)

to make calculations simpler we prefer representing splines in the shifted form, ie 
$$
S_i(x) = a_i + b_i(x-x_i) + c_i(x-x_i)^2 + d_i(x-x_i)^3
$$
-----------------------------
Assignment_01 : Interpolation without libraries
Given - 4 discrete points in increasing orders of x.
We need to find 3 cubic polynomials. $S_0, S_1, S_2$
------------------------