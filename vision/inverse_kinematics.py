import math 
import numpy as np
from tqdm import tqdm


l1 = 10
l2 = 10
l3 = 10

base_height = 10

a1 = 87
a2 = 118
a3 = 147


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

input('Ki obostha?')

position_mat = distance

accuracy = 10000000
req_angle = [0 ,0, 0]

for a1 in range(181):
    for a2 in range(181):
        for a3 in range(181):

            angle_mat = [[math.cos(math.radians(a1)), math.sin(math.radians(a1))],
                        [math.cos(math.radians(a1)+math.radians(a2)), math.sin(math.radians(a1)+math.radians(a2))],
                        [math.cos(math.radians(a1)+math.radians(a2)+math.radians(a3)), math.sin(math.radians(a1)+math.radians(a2)+math.radians(a3))]]

            B = np.array(angle_mat)

            distance = np.matmul(A,B)
            error = math.sqrt((position_mat[0,0] - distance[0,0])**2 + (position_mat[0,1] - distance[0,1])**2)
            
            if(error < accuracy):
                accuracy = error
                req_angle = [a1, a2, a3]
    
    print(a1, req_angle, accuracy)

print(req_angle)
print(accuracy) 



