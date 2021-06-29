import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func(X, a, b, c, d , e, f):

    x,y = X

    val = a*x*x + b*x + c*x*y + d*y +e*y*y + f 
    
    return val


pixel = [(568, 142), (395,218), (230,60), (320,20), (389,59), (172,301), (106, 152), (475, 150), (159, 59), (485,215)]
table = [(30,30), (10,37), (10,18), (25,0), (25,15), (0,40), (0,30), (30,20), (5,17), (15,37)]


pixel_x = []
pixel_y = []

for x in pixel:
    pixel_x.append(x[0])
    pixel_y.append(x[1])


table_y = []

for x in table:
    table_y.append(x[1])


params, _ = curve_fit(func, (pixel_x , pixel_y), table_y)

print(params)

pred_table = []

for x in pixel:
    pred_table.append(func(x, *params))

plt.plot(table_y)
plt.plot(pred_table)
plt.show()




