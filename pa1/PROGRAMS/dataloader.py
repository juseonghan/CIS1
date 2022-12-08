# reads in data from the data directory. 
"""
    Method to read in data from the data directory. 
    @parameters
        filename the name of the textfile to read in
        
    @output
        num_data an array to specify the number of each of the datapts
        result the numpy array of the raw data 
    
"""
import numpy as np
import os 

def load_calbody(filename):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.abspath(os.path.join(cur_dir, os.pardir))
    data_path = os.path.join(script_dir, "data")

    first = 0
    data = []
    num_data = []

    with open(os.path.join(data_path, filename)) as f: 
        while (line := f.readline().rstrip()):
            if first == 0: 
                line_str = line.split(",")
                for num in line_str:
                    if first == 3:
                        break
                    num_data.append(int(num)) 
                    first = first + 1
                continue
            line_str = line.split(",")
            line_int = [float(i) for i in line_str]
            data.append(line_int) 

    #num_data an array
    #data a list of list (2d list)
    return num_data, np.array(data) 


def load_calreadings(filename):

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.abspath(os.path.join(cur_dir, os.pardir))
    data_path = os.path.join(script_dir, "data")

    first = 0
    data = []
    num_data = []

    with open(os.path.join(data_path, filename)) as f: 
        while (line := f.readline().rstrip()):
            if first == 0: 
                line_str = line.split(",")
                for num in line_str:
                    if first == 4:
                        break
                    num_data.append(int(num)) 
                    first = first + 1
                continue
            line_str = line.split(",")
            line_int = [float(i) for i in line_str]
            data.append(line_int)

    # result = np.array(data)
    stacked_result = stack_by_frame(data, num_data, 2)

    #num_data an array
    #data a list of list (2d list)
    return num_data, stacked_result 

def load_empivot(filename):

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.abspath(os.path.join(cur_dir, os.pardir))
    data_path = os.path.join(script_dir, "data")

    first = 0
    data = []
    num_data = []

    with open(os.path.join(data_path, filename)) as f: 
        while (line := f.readline().rstrip()):
            if first == 0: 
                line_str = line.split(",")
                for num in line_str:
                    if first == 2:
                        break
                    num_data.append(int(num)) 
                    first = first + 1
                continue
            line_str = line.split(",")
            line_int = [float(i) for i in line_str]
            data.append(line_int)

    # result = np.array(data)
    stacked_result = stack_by_frame(data, num_data, 3)

    #num_data an array
    #data a list of list (2d list)
    return num_data, stacked_result 

def load_optpivot(filename):

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.abspath(os.path.join(cur_dir, os.pardir))
    data_path = os.path.join(script_dir, "data")

    first = 0
    data = []
    num_data = []

    with open(os.path.join(data_path, filename)) as f: 
        while (line := f.readline().rstrip()):
            if first == 0: 
                line_str = line.split(",")
                for num in line_str:
                    if first == 3:
                        break
                    num_data.append(int(num)) 
                    first = first + 1
                continue
            line_str = line.split(",")
            line_int = [float(i) for i in line_str]
            data.append(line_int)

    # result = np.array(data)
    stacked_result = stack_by_frame(data, num_data, 4)

    #num_data an array
    #data a list of list (2d list)
    return num_data, stacked_result 


def stack_by_frame(result, num_data, arg):
    N_frames = 0
    stack = []
    if arg == 2: # calreadings
        N_frames = num_data[3]
        Nd = num_data[0]
        Na = num_data[1]
        Nc = num_data[2] 
        for i in range(N_frames):
            one_stack = result[ i * (Nd+Na+Nc): (i+1) * (Nd+Na+Nc)]
            stack.append(one_stack)     
    elif arg == 3: #empivot 
        Ng = num_data[0] 
        N_frames = num_data[1]
        for i in range(N_frames):
            one_stack = result[i*Ng : (i+1)*Ng]
            stack.append(one_stack)
    else: # optpivot 
        N_frames = num_data[2]
        Nd = num_data[0]
        Nh = num_data[1]
        for i in range(N_frames):
            one_stack = result[i*(Nd+Nh) : (i+1)*(Nd+Nh)]
            stack.append(one_stack)

    return np.array(stack) 


if __name__ == "__main__":
    num, a = load_calbody("pa1-debug-a-calbody.txt")
    print(num)
    print(a)