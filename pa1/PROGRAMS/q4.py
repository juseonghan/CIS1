#Question 4 Method

from rigid_Transformation import rigid_transformation
from dataloader import load_calreadings 
from dataloader import load_calbody
from pivot_calibration import pivot_calibration
from numpy import linalg 
import argparse 
import numpy as np

# uppercase for relative to optical tracker
# lowercase for relative to calibration body 

# D/d: optical marker locations on EM tracker base
# A/a: LED markers locations on calibration object
# C/c: EM markers on calibration object

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--calreading', required=True, help='calreadings dataset textfile ')
    parser.add_argument('--calbody', required=True, help='calbody dataset textfile ')

    args = parser.parse_args()

    num_calreadings, cal_readings = load_calreadings(args.calreading)
    num_calbody, cal_body = load_calbody(args.calbody)

    d_j = cal_body[0:num_calbody[0], :]
    a_j = cal_body[num_calbody[0]:num_calbody[0] + num_calbody[1], :]

    R_D_stacked = np.array([])
    p_D_stacked = np.array([])
    R_A_stacked = np.array([])
    p_A_stacked = np.array([])

    first = 0 
    # loop through every frame
    for frame in cal_readings:
        D_j = frame[0:num_calreadings[0], :]
        A_j = frame[num_calreadings[0]:num_calreadings[0] + num_calreadings[1], :]

        # calculate R, p from d_j to D_j and a_j to A_j 
        R_D, p_D = rigid_transformation(D_j, d_j)
        R_A, p_A = rigid_transformation(A_j, a_j)

        # stack all R's and p's together
        if first == 0:
            R_D_stacked = R_D
            p_D_stacked = p_D 
            R_A_stacked = R_A
            p_A_stacked = p_A 
            first = first + 1
            continue

        np.concatenate((R_D_stacked, R_D), axis=1)
        np.append(p_D_stacked, p_D, axis=0)

        np.concatenate((R_A_stacked, R_A), axis=1)
        np.append(p_A_stacked, p_A, axis=0)

    # linear least squares to get the average R and p 
    # print(R_D_stacked)
    # print(p_D_stacked)
    # print(R_A_stacked)
    # print(p_D_stacked)

    F_D = pivot_calibration(R_D_stacked, p_D_stacked)
    F_A = pivot_calibration(R_A_stacked, p_A_stacked)

    print(F_D)
    print(F_A)

    # compute C_i expected
    c_i = cal_body[num_calbody[0]+num_calbody[1]:num_calbody[0]+num_calbody[1]+num_calbody[2], :]

    C_i_expected = np.linalg.inv(F_D) @ F_A @ c_i 
    print(C_i_expected)

if __name__ == "__main__":
    main() 