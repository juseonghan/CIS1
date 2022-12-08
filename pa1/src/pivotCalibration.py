import numpy as np
from numpy import linalg 
import math 
from frameTransform import Frame
from pointsetRegistration import Rigid_Transformation

class pivotCalibration():
    
    def __init__(self, pivot, g):
        self.data = pivot
        self.local_frame_data = g
        self.frames = len(pivot)

    def LSE(self,R,p):
        b = np.linalg.inv(R.T @ R) @ R.T @ p
        return np.round(b,2)


    def Calibrate(self):
        ## Matrices to store the Frame transformation across frames
        R_matrices = np.array([[0, 0, 0, 0, 0, 0]])
        p_vectors = np.array([[0]])
        

        G = self.data[0][0] ## 3 X 6

        g = self.local_frame_data

        for i in range(self.frames):
            G = self.data[i][0] ## 3 X 6

            # generating frame transformation F, where F.g = G
            F_getter = Rigid_Transformation(g,G)                                            
            F = F_getter.getTransform()
            # e = F.R @ g + F.p - G

            ## Setting up the LHS for solving pivot calibration
            RotationForLHS = np.concatenate((F.R, -1*np.identity(3)), axis = 1)
            R_matrices = np.append(R_matrices, RotationForLHS, axis=0)
            ## Setting up the RHS for solving pivot calibration
            p_vectors = np.append(p_vectors, F.p, axis=0)


        R_LHS = R_matrices[1:,:]
        p_RHS = -p_vectors[1:,:]

        return self.LSE(R_LHS,p_RHS)


    # q is the values returned by sensor
    # p is the ground truth
    # attempt to find the distortion correction function
    def DistortionCorrection(self, p, q):

        # step 1: scale the values from 0 to 1
        q_scaled = self.ScaleToBox(q)
        
        # step 2: set up the least squares problem
        B = self.ListToNumpy(p) 
        A = self.BernsteinInterpolation(q_scaled)
        
        C = np.linalg.lstsq(A,B, rcond=None) # C is a 556 x 3 matrix 

        # step 3: construct the correction function and return
        return self.convertToFunction(C, q_scaled)

    def convertToFunction(self, c, u):
        result = np.zeros(3) 

        index = 0
        for c_i in c:

            # need to get i,j,k from index
            temp = index 
            k = temp % 10
            temp = temp // 10 
            j = temp % 10 
            temp = temp // 10 
            i = temp % 10 
            temp = temp // 10 

            u_i = u[i]

            b_const = self.Bernstein(u_i[0], i) *self. Bernstein(u_i[1], j) * self.Bernstein(u_i[2], k)

            temp = c_i * b_const 

            result = np.add(result, temp)

        return result 


    def BernsteinInterpolation(self, arr):
        result = np.zeros((len(arr), 556))
        row_num = 0 
        for vec in arr:
            for num in range(556):

                # get the hundredth place, tens place, ones place 
                temp = num 
                k = temp % 10
                temp = temp // 10 
                j = temp % 10 
                temp = temp // 10 
                i = temp % 10 
                temp = temp // 10 

                F_ijk = self.Bernstein(vec[0], i) *self. Bernstein(vec[1], j) * self.Bernstein(vec[2], k)

                result[row_num, num] = F_ijk

            row_num = row_num + 1

        return result 


    def ListToNumpy(self, arr):
        result = np.zeros((len(arr), 3))
        i = 0
        for vec in arr:
            result[i, 0] = vec[0]
            result[i, 1] = vec[1]
            result[i, 2] = vec[2] 
            i = i + 1
        return result 

    def ScaleToBox(self, vec):

        # note that "vec" is a list of numpy arrays 
        # first get each x, y, z list 

        x_list = []
        y_list = []
        z_list = []

        for v_i in vec: 
            x_list.append(v_i[0])
            y_list.append(v_i[1])
            z_list.append(v_i[2])

        
        # calculate the min and max values of x y and z

        x_min = min(x_list) 
        x_max = max(x_list) 
        y_min = min(y_list) 
        y_max = max(y_list) 
        z_min = min(z_list) 
        z_max = max(z_list)  

        x_scaled = []
        y_scaled = []
        z_scaled = []

        # rescale the values 
        for x in x_list:
            x_i = (x - x_min) / (x_max - x_min)
            x_scaled.append(x_i)
        
        for y in y_list:
            y_i = (y - y_min) / (y_max - y_min)
            y_scaled.append(y_i)

        for z in z_list:
            z_i = (z - z_min) / (z_max - z_min)
            z_scaled.append(z_i)


        # put them into a new array and return 
        vec_scaled = []
        
        for i in range(len(x_list)):
            vec_scaled[i] = np.array([ x_scaled[i], y_scaled[i], z_scaled[i] ])

        return vec_scaled 

    def Bernstein(self, u, i):
        return self.choose(5, i) * (u ** i) * ((1-u) ** (5-i)) 


    def choose(n,k):
        num = math.factorial(n)
        den = math.factorial(k)*math.factorial(n-k)
        return num/den
