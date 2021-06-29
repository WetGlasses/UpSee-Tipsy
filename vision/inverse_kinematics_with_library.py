import numpy as np
import tinyik

arm = tinyik.Actuator(['z', [1., 0., 0.], 'z', [1., 0., 0.]])
print(np.rad2deg(arm.angles))

arm.ee = [1.0 , 0.1, 0.]
print(np.round(np.rad2deg(arm.angles)))

#arm.angles = np.deg2rad([-12. , 100.])
print(arm.ee)
