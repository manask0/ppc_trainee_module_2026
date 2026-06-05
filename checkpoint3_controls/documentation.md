## PID (Potential - Integral - Derivative Control)
Calculates an error value as the difference between a desired setpoint and a measured process variable.
$$

u(t) = K_p e(t) + K_i \int_0^t e(\tau)d\tau + K_d \frac{de(t)}{dt}

$$
Where:
- **Kp**: Proportional gain
- **Ki**: Integral gain
- **Kd**: Derivative gain
- **e(t)**: Error = Setpoint - Current Value
![[Pasted image 20260605154025.png]]
Proportional controller : eg- velocity (speed) = k \* (desired loc - current loc)
As a result, current loc asymptotically tends to desired loc, and velocity tends to 0. 
Problem : For a drone, at some height, force due to propellers = gravity, and it would be stuck before desired height. This is called steady state error. 
This can be combated using an integral term, that acts as a memory of what has happened before. If drone reaches steady state below desired height, it has a constant error that increased when integrated.
However, drone path may not be ideal. Integrator may have integrated to a height above desired height (where it would've reached steady state, based on error terms etc)
Now, this negative error when summed will lower the integral term. 
Derivative component tried to predict the future. It produces rate of change of error. 

----
Some possible problems :
a) If the actuator (that we command, eg motor or heater) can saturate (eg motor with max rpm). 
This is called integral windup. Eg, drone-> if we turn it on and then hold, it's possible that the error term accumulates and demands a speed that the propellers can't reach. This will cause trouble once the error becomes negative, because we may end up reducing but still stay above the propeller's limit. ![[Pasted image 20260605155551.png]]
We need an anti-windup method. The idea is to keep the integrator value from crossing a specified limit. 
eg : Clamping : Turning integrator off when it's not needed. Attained through conditional integration. 
![[Pasted image 20260605155938.png]]
Leave some room while setting integrator saturation limit (just in case actuator limit reduces due to temp, age, etc.)

Noise : Random disturbance to signal.
White noise - equal intensity at different frequencies. 

If the sensor is measuring a smooth signal, noise may make it jagged. Derivatives amplify high freq signals, so noise in these will cause problems. (imagine from graph, why high freq has higher derivative) 
Lowering amp of high freq will prevent derivative from increasing.
Using fourier transform, we'll get y' = sigma ai wi

We use a filter that cuts off signals above a certain freq

N/(S+N) -> Low pass filter with cutoff frequency N. 
>We can implement low pass filter with derivative(more readable), or a feedback loop with an integral in the feedback loop(more efficient). (Not sure what this means)
>TO read : impact of each of K_p, Ki_i, K_d

goals : 
- Reach the target speed quickly.
- Not overshoot too much.
- Not oscillate.
- Settle quickly.
- Eliminate steady-state error.
PID tuning is adjusting K_p, K_i, K_d until those goals are met.

More P : Less time
More stability, less overshoot : More D
![[Pasted image 20260605173702.png]]


## Pure Pursuit
The idea behind Pure Pursuit is to compute the steering angle that moves the **rear axle** of the vehicle toward a **goal point** on the path that is a fixed **lookahead distance** ahead of the vehicle.
Think of it like this: when you drive a car, you don't stare at the road directly in front of your bumper — you look some distance ahead and steer toward that point. Pure Pursuit formalises this idea.
  

Given:
- $(x, y)$: rear axle position of the vehicle
- $\psi$: vehicle heading angle (yaw)
- $L$ : wheelbase of the vehicle
- $l_d$ : lookahead distance — how far ahead on the path we pick the goal point
- $(g_x, g_y)$: the goal point on the path at distance $l_d$ from the vehicle
- $\alpha$: the angle between the vehicle's heading and the line from the rear axle to the goal point

The angle $\alpha$ is computed as:  
$$

\alpha = \arctan2(g_y - y, \; g_x - x) - \psi

$$
Using the bicycle model, the steering angle $\delta$ that drives the vehicle along a circular arc through the goal point is given by:
$$

\delta = \arctan\left(\frac{2 \, L \, \sin(\alpha)}{l_d}\right)

$$
Where:
- $L$ is the wheelbase (distance between front and rear axles).
- $l_d$ is the lookahead distance; a larger $l_d$ produces smoother but less responsive tracking, while a smaller $l_d$ tracks the path more tightly but can oscillate.
- $\alpha$ is the angle between the vehicle heading and the direction to the goal point.
- $\delta$ is the steering angle, which should be clipped to the maximum steering limits of the vehicle.
The lookahead distance $l_d$ is the primary tuning knob:
Small -> may oscillate faster but tighter tracking
Large -> smoother curve but may cut corners
A common strategy is to make $l_d$ proportional to the vehicle speed:
$$

l_d = k_{dd} \cdot v + l_{d,\min}

$$
Where $k_{dd}$ is a gain and $l_{d,\min}$ is a minimum lookahead to prevent instability at low speeds.
![[Pasted image 20260605192044.png]]
