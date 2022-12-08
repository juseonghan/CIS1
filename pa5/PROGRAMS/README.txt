Scripts Overview:

pa5.py - the main script for running the deformable registration algorithm. This is the script that will be ran for execution.
frameTransform.py - Frame class. Defines a transformation [R|p] and some operations
utils.py - contains functions for FindClosestPointOnMesh and BoundingSphere, barycentric manipulation, lambda calculations, and other helper functions.
Octree.py - contains an implementation of the octree data structure
pointsetRegistration.py - contains 3D point cloud to point cloud registration using the Quanternion method
test.py - the test script for running tests for certain functions, such as read, write, findclosestPoint, etc. 
reader.py - classes to read data files as inputs and store them into data structures
writer.py - classes to write data files as outputs from data structures
config.ini - config file used for data input specification
__init__.py - empty script for modularization

We used Python 3.8 and Numpy 1.21 for the assignment. 

To run the code, simply change the contents of config.ini to the desired file. Then, simply run 

$ python pa5.py

Similarily, one could use

$ python test.py 

to run the test scripts. 
