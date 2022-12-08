#Question 5 Method

from rigid_Transformation import rigid_transformation
from dataloader import *
from pivot_calibration import pivot_calibration
from numpy.linalg import inv
import argparse 


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--empivot', required=True, help='calreadings dataset textfile ')
    args = parser.parse_args()

    num, G = load_empivot(args.empivot)

    R_ks = []
    p_ks = []

    #Get All the F[k] and stack it up in a list
    for frame in G:
        frame_mean = np.mean(frame, axis = 0)
        
        

        g = frame - frame_mean
        
        R, p = rigid_transformation(frame,g)
        

		p_ks.append(p)

        p_ks.append(p)

    
    R_ks = np.array(R_ks).T
    p_ks = -1*np.array(p_ks).T

    print(R_ks.shape)
    b = pivot_calibration(R_ks,p_ks)
    # print(b)