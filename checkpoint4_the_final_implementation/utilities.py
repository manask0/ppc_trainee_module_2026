import numpy as np
import math

class PIDController:
    """PID controller for throttle (velocity tracking)."""

    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, error, dt):
        self.integral+=error*dt
        derivative = (error-self.prev_error)/dt
        output = self.Kp * error + self.Ki * self.integral +self.Kd * derivative
        self.prev_error = error
        
        return output





def pure_pursuit_steering(x, y, yaw, v, waypoints, L=2.5, k_dd=0.5, ld_min=2.0, max_steer=np.radians(30)):
    ld = k_dd*v+ld_min
    nearest_index=0
    least_distance = None
    i = 0
    for i in range (len(waypoints)):
        dist = ((waypoints[i][0]-x)**2+(waypoints[i][1]-y)**2)**0.5
        if (least_distance == None) or (dist < least_distance):
            least_distance = dist
            nearest_index = i

    target_idx = len(waypoints) - 1
    for i in range(nearest_index, len(waypoints)):
        dist = ((waypoints[i][0]-x)**2+(waypoints[i][1]-y)**2)**0.5
        if dist>ld:
            target_idx = i
            break
    goal_x = waypoints[target_idx][0]
    goal_y=waypoints[target_idx][1]


    alpha = np.arctan2(goal_y - y, goal_x - x) - yaw
    alpha = math.remainder(alpha, math.tau)
    steer = np.arctan2(2 * L * np.sin(alpha), ld)

    steer = np.clip(steer,-1*max_steer,max_steer)

    return steer, target_idx
