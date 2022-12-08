from rigid_Transformation import rigid_transformation
from dataloader import load_data
from pivot_calibration import pivot_calibration

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--data1', required=True, help='first point cloud textfile name')
    parser.add_argument('--data2', required=True, help='second point cloud textfile name')

    args = parser.parse_args()
    
	n1, em_pivot_data = load_data(args.data1)
    n2, opt_pivot_data = load_data(args.data2)
    
    R_lhs = np.array([])
    p_lhs = np.array([])
    
    for i in range(len(em_pivot_data)):
    	R, p = rigid_transformation(em_pivot_data[i], opt_pivot_data[i])
    	
    	R = np.concatenate(R, -1*np.identity(3), axis = 1)
    	R_lhs = np.append(R_lhs, R, axis = 0)
    	p_lhs = np.append(p_lhs, p, axis = 0)

    b = pivot_calibration(R_lhs,p_lhs)
    
    print(b)


