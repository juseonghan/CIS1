from rigid_Transformation import rigid_transformation
import numpy as np 


def main(): 

    data1 = "pa1-debug-a-empivot.txt"
    data2 = "pa1-debug-a-optpivot.txt"
    n1, em_pivot_data = load_data(data1, 3)
    n2, opt_pivot_data = load_data(data2, 4)

    N_frames = n1[1] 
    
    for i in range(N_frames):
        


if __name__ == "__main__":
    main()