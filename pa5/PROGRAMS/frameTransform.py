import numpy as np
from numpy import linalg

class Frame():
    
    #initialization
    def __init__(self, rotation, translation):
        
        self.R = rotation
        self.p = translation
        
    def MSE(self, secondFrame):
        my_t = self.p[...,None]
        second_t = secondFrame.p[...,None]
        my_combined = np.hstack((self.R, my_t))
        second_combined = np.hstack((secondFrame.R, second_t))

        diff_norm = np.linalg.norm(my_combined - second_combined)
        return diff_norm 

    #return a frame object representing the inverse transformation
    def F_inv(self):
        R_inv = self.R.T
        T_inv = np.dot(-R_inv, self.p)
        return Frame(rotation=R_inv,translation=T_inv)
    
    #returns the result of 2 frame composition
    def ComposeTransform(self, secondFrame):
        R_res = np.dot(self.R, secondFrame.R)
        P_res = np.add(np.dot(self.R, secondFrame.p), self.p)
        return Frame(rotation=R_res, translation=P_res)
    
    #returns the vector resulting from the frame transformation
    def transformVector(self, v):
        p = np.add(np.dot(self.R, v), self.p)
        return p

   