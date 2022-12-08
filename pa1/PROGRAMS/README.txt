## John Han and Unnat Antani CIS Programming Assignment #1 

rigid_Transformation.py: function/script to invoke for computing the 3D point cloud to point cloud registration using the Quaternion method
pivot_calibration.py: function/script to invoke for computing the calibration algorithm for pivot pointer
dataloader.py: functions to invoke for reading in data in an organized and modularized fashion
q4.py: python script for question 4
q5.py: python script for question 5

Prerequisities: 
Python 3.8+ 
NumPy 1.21

These were used for the execution and testing of the code. Python virtual environments or conda environment may prove useful.
eg you can create a conda environment and install dependencies by:
$ conda create --name cis_pa1 python=3.8
$ conda activate cis_pa1
$ pip3 install numpy==1.21

For running our code, we used q4.py and q5.py, which invokes functions from dataloader, rigid_transformation, and pivot_calibration. 
To run q4.py on pa1-debug-a-calreadings.txt and pa1-debug-a-calbody.txt for example,:
$ python q4.py --calreading "pa1-debug-a-calreadings.txt" --calbody "pa1-debug-a-calbody.txt"
will run the script using those two datasets. The same applies to q5.py. q4,q5,q6 was not completed.  

