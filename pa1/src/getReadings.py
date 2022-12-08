
import numpy as np

def getValues(line):
    data = line.split(',')
    return np.array([[float(data[0]), float(data[1]), float(data[2])]], dtype=np.float32)


#Stack up data for each frame and return an array of each frame as its element
def getDataFromFile(filename, mulFrames=True):
    outdata = []
    
    with open(filename) as f:
        count = 0
        lines = f.readlines() #Get the lines
        header = lines[count].split(',') #Read header to get information
        n_arr = header[:-1] #Number of frames
        
        if not mulFrames:
            n_arr.append("1")
        
        readings_per_frame = len(n_arr) - 1 #Ignoring the first reading as per Piazza suggestion
        lines_per_frame = 0 #Counter for number of readings per frame
        
        for i in n_arr[:-1]:
            lines_per_frame += int(i)
            
        count += 1
        
        for j in range(int(n_arr[-1])):
            
            frame_Readings = []
            for i in range(readings_per_frame):
                frame_Readings.append(np.array([[0, 0, 0]], dtype=np.float32).T)
            
            count = 1 + j *  lines_per_frame
            for line in lines[count:]:
            
                point = getValues(lines[count]).T
                
                for i in range(readings_per_frame):
                    if len(frame_Readings[i][0]) < int(n_arr[i]) + 1:
                        frame_Readings[i] = np.append(frame_Readings[i], point, axis=1)
                        break
            
                count += 1
            
            inter = []
    
            for a in frame_Readings:
                inter.append(a[:,1:])
                
            outdata.append(inter)
            
        f.close()
   
    return outdata