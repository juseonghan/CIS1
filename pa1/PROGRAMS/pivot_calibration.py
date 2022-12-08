import numpy as np 
from numpy import linalg


#Using least square solutions of Numpy
#Input - Array of Rotation matrices augmented with Identity Matrices
#And position matrices
#Output - Least sqaures fit for b_tip and b_post
#b = [b_tip b_post]
def pivot_calibration(R, p):
    # print(R)
    # print(p)

    R = R[1:,:]
    p = p[1:,:]

    b = np.linalg.inv(R.T @ R) @ R.T @ p

    return np.round(b,2)
