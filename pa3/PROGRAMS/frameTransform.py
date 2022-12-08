import numpy as np
class Frame():
    
    #initialization
    def __init__(self, rotation, translation):
        
        self.R = rotation
        self.p = translation
        
        
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

   