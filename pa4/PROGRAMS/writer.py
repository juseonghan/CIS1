import numpy as np 

"""
    Function to write the output
"""

def outputWriter(N_samples, title, data1, data2, data3):
    with open(title, "w") as fid:
        fid.write(str(N_samples) + "," + title[-16:] + "\n")

        for line1, line2, val in zip(data1, data2, data3):

            t1 = [ '%.2f' % elem for elem in line1]
            temp1 =  ['{0: <9}'.format(i) for i in t1]
            fid.write(''.join(temp1))
            fid.write('\t\t')

            t2 = [ '%.2f' % elem for elem in line2]
            temp2 =  ['{0: <9}'.format(i) for i in t2]
            fid.write(''.join(temp2))
            fid.write('\t\t')

            temp3 = "%0.2f" % val 
            fid.write(temp3)
            fid.write('\n')
        fid.write("\n")
