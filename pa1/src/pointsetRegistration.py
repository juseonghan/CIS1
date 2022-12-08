
import numpy as np
from frameTransform import Frame
from numpy import linalg as LA 


class Rigid_Transformation():

    def __init__(self, a, b):


        self.a = a
        self.b = b
        self.N = self.a.shape[1]

        #Finding mean of the data
        self.a_bar = np.zeros((3, 1), dtype=np.float32)
        self.b_bar = np.zeros((3, 1), dtype=np.float32)

        for i in range(3):
            self.a_bar[i][0] = np.sum(self.a[i], dtype=np.float32) / self.N
            self.b_bar[i][0] = np.sum(self.b[i], dtype=np.float32) / self.N

        
        #Generating tilda matrices to be used for the quaternion method
        self.a_tilda = self.a - self.a_bar 
        self.b_tilda = self.b - self.b_bar 
     
        
    #Helper function to convert quaternion to rotation matrix
    def quat_to_rotation(self,q):
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
        
    #Main function which solves and returns R and P: Quaternion Method
    def solve(self):
        
        # step 1: compute H matrix
        H = np.zeros((3,3))
        
        for _a, _b in list(zip(self.a_tilda, self.b_tilda)): 
            H_temp = np.array([[_a[0]*_b[0], _a[0]*_b[1], _a[0]*_b[2]], 
                            [_a[1]*_b[0], _a[1]*_b[1], _a[1]*_b[2]], 
                            [_a[2]*_b[0], _a[2]*_b[1], _a[2]*_b[2]]])
        
            H = np.add(H, H_temp)
        
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


        # Convert quaternion to Rotation Matrix
        self.R = self.quat_to_rotation(rotation_quat)
        # print(self.R)
        
        #Use Rotation matrix and calculate the translation
        self.p = np.add(self.b_bar,-self.R @ self.a_bar) 
        # print(self.p)
        
        return self.R, self.p
    
    #calls solve function, returns the frame object of containing R and p
    def getTransform(self):

        R, p = self.solve()
        return Frame(R, p)
