import math 
import numpy as np


l1 = 1
l2 = 1
l3 = 0

base_height = 10

a1 = 60
a2 = 60
a3 = 0


a1 = math.radians(a1)
a2 = math.radians(a2)
a3 = math.radians(a3)


x_dist = (l1 * math.cos(a1)) - (l2 * math.cos(a1 + a2)) + (l3 * math.cos(a1 + a2 + a3))
y_dist = (l1 * math.sin(a1)) - (l2 * math.sin(a1 + a2)) + (l3 * math.sin(a1 + a2 + a3))


length_mat = [[l1, -l2, l3]]
angle_mat = [[math.cos(a1), math.sin(a1)],
            [math.cos(a1+a2), math.sin(a1+a2)],
            [math.cos(a1+a2+a3), math.sin(a1+a2+a3)]]

A = np.array(length_mat)
B = np.array(angle_mat)

distance = np.matmul(A,B)

print(distance)

print(x_dist, y_dist)