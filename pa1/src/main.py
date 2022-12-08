import numpy as np
from pointsetRegistration import Rigid_Transformation
import getReadings as get
from pivotCalibration import pivotCalibration
from frameTransform import Frame

#Function to get the relevant data
def CleanCalData(calreadings):
    D = []
    A = []
    C = []
    for frame in calreadings:
        D.append(frame[0])
        A.append(frame[1])
        C.append(frame[2])
    return D, A, C

#Calculate Cis
def C_Expected(calbody, calreadings):

    d = calbody[0][0]
    a = calbody[0][1]
    c = calbody[0][2]
    
    D, A, C = CleanCalData(calreadings)
        
    F_ds = []
    F_as = []
    C_list = []
        
    for i in range(len(D)):
        
        F_d = Rigid_Transformation(d, D[i]).getTransform()
        F_ds.append(F_d)
        
       
        F_a = Rigid_Transformation(a, A[i]).getTransform()
        F_as.append(F_a)
        
       
        C_j_list = np.array([[0, 0, 0]]).T
        
        for j in range(len(c[0])):
            cj_vector = np.array([c[:,j]]).T
            C_exp = F_d.F_inv().ComposeTransform(F_a).transformVector(cj_vector)
            C_j_list = np.append(C_j_list, C_exp, axis=1)
            
        C_list.append(C_j_list[:,1:])
        
    return C_list


#Generate g = G - Avg(G)
def gengvector(data):
    G = data[0][0] # Size = 3 X 6
    # print(G.shape)
    G_bar = np.mean(G, axis = 1) # get the avg along the columns Size = 3 X 1
    # print(G_bar.shape)
    
    g = np.array([[0, 0, 0]]).T #Creating empty g

    #calculating g
    for j in range(len(G[0])):
        g_inter = np.add(G[:,j], -G_bar)
        g = np.append(g, np.array([g_inter]).T, axis=1)

    g = g[:,1:] #Ignoring the first element as per Piazza suggestion
    
    return g


def b_post_EM(empivot):
    g = gengvector(empivot)
    solver = pivotCalibration(empivot,g)
    b = solver.Calibrate()
    return b

# function to convert to the EM tracker coordinates
def ChangetoEM(optpivot,d):
    data = []
    for i in range(len(optpivot)):
        D = optpivot[i][0]
        
       
        F = Rigid_Transformation(D,d).getTransform()

        ## Array to store the position after transformation
        H_new = np.array([[0, 0, 0]])
        H = optpivot[i][1]
        for j in range(len(H[0])):
            
            u = F.R @ H[:,j] + F.p.T
            H_new = np.append(H_new, u, axis = 0)
        H_d = []
        H_d.append(H_new[1:,:].T)
        data.append(H_d)
    return data

def b_post_opt(calbody, optpivot):

    d1 = calbody[0][0]
    data = ChangetoEM(optpivot,d1)
    b = b_post_EM(data)
    return b


#main function for generation of the output file
if __name__ == '__main__':
    
    ParDir = '../data/' #Parent Directory for accessing the data
    
    # Change filenames here
    
    calbodyPath = ParDir + "NAME-CALBODY.TXT"
    calreadingsPath = ParDir +  "NAME-CALREADINGS.TXT"
    empivotPath = ParDir +  "NAME-EMPIVOT.TXT"
    optpivotPath = ParDir +  "NAME-OPTPIVOT.TXT"
    
    #Load data from text files
    
    calbody = get.getDataFromFile(calbodyPath, mulFrames=False)
    calreadings = get.getDataFromFile(calreadingsPath)
    empivot = get.getDataFromFile(empivotPath)
    optpivot = get.getDataFromFile(optpivotPath)
    
    
    #All values rounded off to 2 decimal points
    C_expected = np.round(C_Expected(calbody, calreadings),2) 
    B_post_EM = np.round(b_post_EM(empivot)[3:6,:],2)
    B_post_opt = np.round(b_post_opt(calbody, optpivot)[3:6,:],2)
    
    #Get the header information - number of vectors, number of frames
    N_frames = len(C_expected)
    N_C = len(C_expected[0][0])
        
    
    #Create output file name and path
    outputFileName = "NAME-OUTPUT-1.TXT"
    outputPath = "../output/"+ outputFileName
    
    '''
    ####Writing the generated output in the same format as the input data####
    
    Header will include information of number of vectors, number of frames and the output file name
    Followed by the generated output data values for EM Tracker
    Followed by generated output data values for Optical Tracker
    Followed by the expected values of the Ci vectors    
    
    '''
    
    with open(outputPath, 'w') as f:

        f.write(f"{N_C}, {N_frames},{outputFileName}\n")
        f.write(f"{B_post_EM[0][0]},{B_post_EM[1][0]},{B_post_EM[2][0]}\n")
        f.write(f"{B_post_opt[0][0]},{B_post_opt[1][0]},{B_post_opt[2][0]}\n")
        
        #Write the expected values
        for _ in C_expected:
            for i in range(N_C):
                f.write(f"{_[0][i]},{_[1][i]},{_[2][i]}\n")
        f.close()  
    
    print("Output Recorded !")