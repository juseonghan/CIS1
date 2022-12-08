from IterativeClosestPoint import FindClosestPointMesh
from IterativeClosestPoint import FindClosestPointMesh_BS
from pointsetRegistration import Rigid_Transformation
from frameTransform import Frame
from writer import outputWriter
import reader
import numpy as np 
import os 
from os import path 
import time 
import configparser
import argparse


def validate_file(f):
    if not os.path.exists(f):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f


def slow_ICP(paths):

    start = time.time()
    print('RUNNING SLOW_ICP')
    print('Reading in datafiles...')
    bodyA = reader.BodyLEDs(paths[0]) 
    bodyB = reader.BodyLEDs(paths[1]) 
    mesh = reader.SurfaceMesh(paths[2]) 
    sample_readings = reader.SampleReadings(paths[3])

    print('BodyA datafile: ' + paths[0])
    print('BodyB datafile: ' + paths[1])
    print('Mesh datafile: ' + paths[2])
    print('Readings datafile: ' + paths[3])

    # outputs 
    C = []
    D = []
    Norm = []

    count = 0
    origin = []
    origin.append(np.array([0,0,0]))

    for frame_k in sample_readings.N:
        print("Frame " + str(count) + " processing...")
        a_k = frame_k[0:bodyA.N_markers, :]
        b_k = frame_k[bodyA.N_markers:bodyA.N_markers + bodyB.N_markers,:]
        #dummy_k = frame_k[-(sample_readings.N_samples - bodyA.N_markers - bodyB.N_markers), :]
        
        a_k = list(a_k)
        b_k = list(b_k)

        print("Performing Point Cloud Registrations...")
        # point cloud registration to find F_Ak
        # F_trackerToBody = F_trackerToLEDs * F_bodyToLEDs^-1
        F_trackerToLEDs = Rigid_Transformation(origin, a_k).getTransform()
        F_bodyToLEDs = Rigid_Transformation(origin, bodyA.Y).getTransform()
        F_Ak = F_trackerToLEDs.ComposeTransform(F_bodyToLEDs.F_inv())

        # point cloud registration to find F_Bk
        F_trackerToLEDs = Rigid_Transformation(origin, b_k).getTransform()
        F_bodyToLEDs = Rigid_Transformation(origin, bodyB.Y).getTransform()
        F_Bk = F_trackerToLEDs.ComposeTransform(F_bodyToLEDs.F_inv())

        # calculate d_k, the transformation from rigid body to pointer
        F_AB = F_Bk.F_inv().ComposeTransform(F_Ak) 
        d_k = F_AB.transformVector(bodyA.t)

        # first, F_reg is an identity matrix
        F_reg = Frame(np.identity(3), np.zeros(3))
        eps = 1
        while eps > 0.1:
            F_old = F_reg 
            ss = F_reg.transformVector(d_k)
            cs, tri = FindClosestPointMesh(ss, mesh.verts, mesh.tris)
            F_reg = Rigid_Transformation(d_k, cs).getTransform()
            eps = F_reg.MSE(F_old)
            
        s_k = F_reg.transformVector(d_k)

        print("Executing ICP...")
        # calculate c, the points on the surface mesh closest to s_k
        c_k, tri = FindClosestPointMesh(s_k, mesh.verts, mesh.tris)

        # append to output lists
        norm = np.linalg.norm(c_k - d_k)
        C.append(c_k)
        D.append(d_k)
        Norm.append(norm)
        count = count + 1 

    # write output to file
    letter = paths[3].split('-')[1]
    output_filename = "pa3-"+letter+"-Output.txt"

    fileDir = os.path.dirname(os.path.realpath(__file__))
    relpath = "../OUTPUT/" + output_filename 
    filename = os.path.join(fileDir, relpath)
    filename = os.path.abspath(os.path.realpath(filename))

    print("Printing output to: " + filename)

    outputWriter(sample_readings.N_samples, filename, C,D,Norm)

    end = time.time() - start

    print("Done in " + str(end) + " seconds.")

    

def fast_ICP(paths):

    start = time.time() 
    print('RUNNING FAST_ICP')
    print('Reading in datafiles...')
    bodyA = reader.BodyLEDs(paths[0]) 
    bodyB = reader.BodyLEDs(paths[1]) 
    mesh = reader.SurfaceMesh(paths[2]) 
    sample_readings = reader.SampleReadings(paths[3])

    print('BodyA datafile: ' + paths[0])
    print('BodyB datafile: ' + paths[1])
    print('Mesh datafile: ' + paths[2])
    print('Readings datafile: ' + paths[3])

    # outputs 
    C = []
    D = []
    Norm = []

    count = 0
    origin = []
    origin.append(np.array([0,0,0]))

    for frame_k in sample_readings.N:
        print("Frame " + str(count) + " processing...")
        a_k = frame_k[0:bodyA.N_markers, :]
        b_k = frame_k[bodyA.N_markers:bodyA.N_markers + bodyB.N_markers,:]
        #dummy_k = frame_k[-(sample_readings.N_samples - bodyA.N_markers - bodyB.N_markers), :]
        
        a_k = list(a_k)
        b_k = list(b_k)

        print("Performing Point Cloud Registrations...")
        # point cloud registration to find F_Ak
        # F_trackerToBody = F_trackerToLEDs * F_bodyToLEDs^-1
        F_trackerToLEDs = Rigid_Transformation(origin, a_k).getTransform()
        F_bodyToLEDs = Rigid_Transformation(origin, bodyA.Y).getTransform()
        F_Ak = F_trackerToLEDs.ComposeTransform(F_bodyToLEDs.F_inv())

        # point cloud registration to find F_Bk
        F_trackerToLEDs = Rigid_Transformation(origin, b_k).getTransform()
        F_bodyToLEDs = Rigid_Transformation(origin, bodyB.Y).getTransform()
        F_Bk = F_trackerToLEDs.ComposeTransform(F_bodyToLEDs.F_inv())

        # calculate d_k, the transformation from rigid body to pointer
        F_AB = F_Bk.F_inv().ComposeTransform(F_Ak) 
        d_k = F_AB.transformVector(bodyA.t)
        s_k = d_k

        print("Executing ICP...")
        # calculate c, the points on the surface mesh closest to s_k
        c_k, tri = FindClosestPointMesh_BS(s_k, mesh.verts, mesh.tris)

        # append to output lists
        norm = np.linalg.norm(c_k - d_k)
        C.append(c_k)
        D.append(d_k)
        Norm.append(norm)
        count = count + 1 

    # write output to file
    letter = paths[3].split('-')[1]
    output_filename = "pa4-"+letter+"-Output.txt"

    fileDir = os.path.dirname(os.path.realpath(__file__))
    relpath = "../OUTPUT/" + output_filename 
    filename = os.path.join(fileDir, relpath)
    filename = os.path.abspath(os.path.realpath(filename))

    print("Printing output to: " + filename)

    outputWriter(sample_readings.N_samples, filename, C,D,Norm)

    end = time.time() - start 
    print("Done in " + str(end) + " seconds.")


if __name__ == "__main__":
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    pathtxt = []
    for sect in parser.sections():
        for k,v in parser.items(sect):
            pathtxt.append(v)

    if int(pathtxt[4]) == 0:
        slow_ICP(pathtxt)
    elif int(pathtxt[4]) == 1:
        fast_ICP(pathtxt)
    elif int(pathtxt[4]) == 2:
        fastest_ICP(pathtxt)
    else:
        print('invalid speed in configuration file')
