import numpy as np 

"""
    Function to write the output
"""

def outputWriter(N_samples, title, data1, data2, data3):
    with open(title, "w") as fid:
        fid.write(str(N_samples) + "," + title + "\n")

        for line1, line2, val in zip(data1, data2, data3):
            temp1 = ["%0.2f" % i for i in line1]
            temp_str1 = [str(a) for a in temp1]
            final1 = ','.join(temp_str1)
            fid.write(final1)
            fid.write('\t')

            temp2 = ["%0.2f" % i for i in line2]
            temp_str2 = [str(a) for a in temp2]
            final2 = ','.join(temp_str2)
            fid.write(final2)
            fid.write('\t')

            temp3 = "%0.2f" % val 
            fid.write(str(temp3))
            fid.write("\n")
        fid.write("\n")
