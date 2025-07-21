import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

p1=tuple(map(float, input().split()))
p2=tuple(map(float, input().split()))
p3=tuple(map(float, input().split()))

v1=tuple(map(float, input().split()))
v2=tuple(map(float, input().split()))
v3=tuple(map(float, input().split()))

m = float(input())
timestep = float(input())
# for timestep do not choose absurdly small values
# lest floating point arithmetic bite you in the ass

G = 10

def distance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return ((x2-x1) **2 + (y2-y1) ** 2) ** 0.5

def add(u,v):
    x1,y1 = u
    x2,y2 = v

    return x1+x2, y1+y2

def opposite(u):
    x,y = u
    return -x, -y

def subtract(u,v):
    return add(u, opposite(v))

def gravitational_force(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return G * m ** 2 * (x2-x1) / (distance(p1,p2) ** 3), \
           G * m ** 2 * (y2-y1) / (distance(p1,p2) ** 3)

def acceleration(f):
    x1,y1 = f
    return x1/m, y1/m

def position(initial_position, initial_velocity, acceleration):
    x,y = initial_position
    vx,vy = initial_velocity
    ax,ay = acceleration
    return 1/2 * ax * timestep ** 2 + vx * timestep + x, \
           1/2 * ay * timestep ** 2 + vy * timestep + y

def velocity(initial_velocity, acceleration):
    vx,vy = initial_velocity
    ax,ay = acceleration
    return ax * timestep + vx, \
           ay * timestep + vy


positions = [{'A': p1, 'B': p2, 'C': p3}]
t = 0
while t <= 50:
    acc_AB = acceleration(gravitational_force(p1,p2))
    acc_BA = acceleration(opposite(gravitational_force(p1,p2)))

    acc_AC = acceleration(gravitational_force(p1,p3))
    acc_CA = acceleration(opposite(gravitational_force(p1,p3)))

    acc_BC = acceleration(gravitational_force(p2,p3))
    acc_CB = acceleration(opposite(gravitational_force(p2,p3)))

    new_pos_A = position(p1, v1, add(acc_AB, acc_AC))
    new_pos_B = position(p2, v2, add(acc_BA, acc_BC))
    new_pos_C = position(p3, v3, add(acc_CA, acc_CB))
    new_velocity_A = velocity(v1, add(acc_AB, acc_AC))
    new_velocity_B = velocity(v2, add(acc_BA, acc_BC))
    new_velocity_C = velocity(v3, add(acc_CA, acc_CB))
    positions.append({'A': new_pos_A, 'B': new_pos_B, 'C': new_pos_C})
    p1,p2,p3 = new_pos_A, new_pos_B, new_pos_C
    v1,v2,v3 = new_velocity_A, new_velocity_B, new_velocity_C

    t += timestep


def animate_three_body(positions):
    A_trajectory = [pos['A'] for pos in positions]
    B_trajectory = [pos['B'] for pos in positions]
    C_trajectory = [pos['C'] for pos in positions]

    A_x, A_y = zip(*A_trajectory)
    B_x, B_y = zip(*B_trajectory)
    C_x, C_y = zip(*C_trajectory)

    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('black')

    all_x = list(A_x) + list(B_x) + list(C_x)
    all_y = list(A_y) + list(B_y) + list(C_y)
    x_range = max(all_x) - min(all_x)
    y_range = max(all_y) - min(all_y)
    margin_x = 0.05 * x_range if x_range > 0 else 1
    margin_y = 0.05 * y_range if y_range > 0 else 1
    ax.set_xlim(min(all_x) - margin_x, max(all_x) + margin_x)
    ax.set_ylim(min(all_y) - margin_y, max(all_y) + margin_y)

    line_A, = ax.plot([], [], 'r-', linewidth=1, alpha=0.7, label='Body A')
    line_B, = ax.plot([], [], 'g-', linewidth=1, alpha=0.7, label='Body B')
    line_C, = ax.plot([], [], 'b-', linewidth=1, alpha=0.7, label='Body C')

    point_A, = ax.plot([], [], 'ro', markersize=8, markeredgecolor='white', markeredgewidth=1)
    point_B, = ax.plot([], [], 'go', markersize=8, markeredgecolor='white', markeredgewidth=1)
    point_C, = ax.plot([], [], 'bo', markersize=8, markeredgecolor='white', markeredgewidth=1)

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title('Three-Body Problem Simulation')
    ax.legend()

    def animate_frame(frame): 
        line_A.set_data(A_x[:frame + 1], A_y[:frame + 1])
        line_B.set_data(B_x[:frame + 1], B_y[:frame + 1])
        line_C.set_data(C_x[:frame + 1], C_y[:frame + 1])
 
        if frame < len(positions):
            point_A.set_data([A_x[frame]], [A_y[frame]])
            point_B.set_data([B_x[frame]], [B_y[frame]])
            point_C.set_data([C_x[frame]], [C_y[frame]])

        return line_A, line_B, line_C, point_A, point_B, point_C

    anim = animation.FuncAnimation(
        fig, animate_frame, frames=len(positions),
        interval=1, blit=True, repeat=True
    )

    plt.show()
    return anim

animate_three_body(positions)
