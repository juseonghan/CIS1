""" 
A rigid transformation between two 3D point clouds 

Employs the use of quaternions found on slide 25 on "Rigid3D3DCalculations" 

"""

import numpy as np 
import dataloader
from numpy import linalg as LA 
import argparse

def rigid_transformation(a, b): 
    # first need to calculate a tilda & b tilda for normalization
    a_bar = np.mean(a, axis=0)
    b_bar = np.mean(b, axis=0)

    a_tilda = a - a_bar 
    b_tilda = b - b_bar 

    # step 1: compute H matrix
    H = np.zeros((3,3))
    for _a, _b in list(zip(a_tilda, b_tilda)): 
        H_temp = np.array([[_a[0]*_b[0], _a[0]*_b[1], _a[0]*_b[2]], 
                            [_a[1]*_b[0], _a[1]*_b[1], _a[1]*_b[2]], 
                            [_a[2]*_b[0], _a[2]*_b[1], _a[2]*_b[2]]])
        
        H = H + H_temp 

    # step 2: compute G matrix 
    delta_transpose = np.array([H[1,2] - H[2,1], H[2,0] - H[0,2], H[0,1] - H[1,0]]) 
    delta = np.array([[delta_transpose[0]], [delta_transpose[1]], [delta_transpose[2]]])
    G = np.block([
            [np.trace(H), delta_transpose], 
            [delta, H + np.transpose(H) - np.trace(H)*np.eye(3)]
        ])

    # step 3: compute eigenvalue decomposition of G 
    eigvals, eigvecs = LA.eig(G)

    # step 4: get the rotation quaternion
    _eigvals = np.sum(eigvals, axis=0)
    max_eig_loc = np.argmax(_eigvals) # max_eig_loc is the column # that gives the rotation quaternion
    rotation_quat = eigvecs[:, max_eig_loc]

    # need to convert unit quaternion into rotation matrix
    R = quat_to_rotation(rotation_quat)

    p = b_bar - R @ a_bar 

    # neg_identity = np.array([[-1, 0 ,0], [0,-1,0],[0,0,-1]])
    # R = np.vstack((R, neg_identity))


    return R, p

def quat_to_rotation(q):
    q00 = q[0]**2 + q[1]**2 - q[2]**2 - q[3]**2 
    q01 = 2*(q[1]*q[2] - q[0]*q[3])
    q02 = 2*(q[1]*q[3] + q[0]*q[2])
    q10 = 2*(q[1]*q[2] + q[0]*q[3])
    q11 = q[0]**2 - q[1]**2 + q[2]**2 - q[3]**2 
    q12 = 2*(q[2]*q[3] - q[0]*q[1])
    q20 = 2*(q[1]*q[3] - q[0]*q[2])
    q21 = 2*(q[2]*q[3] + q[0]*q[1])
    q22 = q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2 

    result = np.array([[q00, q01, q02], [q10, q11, q12], [q20, q21, q22]])
    return result


def main(data1, data2): 

    n1, em_pivot_data = dataloader.load_empivot(data1, 3)
    n2, opt_pivot_data = dataloader.load_optpivot(data2, 4)

    R1, p1 = rigid_transformation(em_pivot_data, opt_pivot_data)
    
    print(R1)
    
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--data1', required=True, help='first point cloud textfile name')
    parser.add_argument('--data2', required=True, help='second point cloud textfile name')

    args = parser.parse_args()
    
    main(args.data1, args.data2)
