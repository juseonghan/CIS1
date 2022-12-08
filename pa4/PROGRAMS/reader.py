import numpy as np 
from pathlib import Path
import os
from os import path 

class BodyLEDs:
    """ Parses the Body Marker LED data """

    def __init__(self, path: str):
        fileDir = os.path.dirname(os.path.realpath(__file__))
        self.path = "../data/" + path 
        filename = os.path.join(fileDir, self.path)
        filename = os.path.abspath(os.path.realpath(filename))
        with open(filename, "r") as f:
            line = next(f).split()
            self.N_markers = int(line[0])

        arr = np.loadtxt(filename, skiprows=1, dtype=np.float64)
        self.Y = arr[:-1,:]
        self.t = arr[-1,:]

class SurfaceMesh:
    """ Parses the surface mesh data """

    def __init__(self, path: str):
        fileDir = os.path.dirname(os.path.realpath(__file__))
        self.path = "../data/" + path 
        filename = os.path.join(fileDir, self.path)
        filename = os.path.abspath(os.path.realpath(filename))
        with open(filename, "r") as f:
            self.N_vertices = int(next(f))
            
        self.verts = np.loadtxt(filename, skiprows=1, max_rows=self.N_vertices,dtype=np.float64)
        self.N_triangles = int(np.loadtxt(filename, skiprows=1+self.N_vertices, max_rows=1, dtype=np.int16))
        tris_read = np.loadtxt(filename, skiprows=2+self.N_vertices, dtype=np.int16)
        self.tris = tris_read[:,0:3]

class SampleReadings:
    """ Parses the sample reading data """

    def __init__(self, path: str):
        fileDir = os.path.dirname(os.path.realpath(__file__))
        self.path = "../data/" + path 
        filename = os.path.join(fileDir, self.path)
        filename = os.path.abspath(os.path.realpath(filename))
        with open(filename, "r") as f:
            line = next(f).split(",") 
            self.N_s = int(line[0])
            self.N_samples = int(line[1])
        
        self.N = []
        for i in range(self.N_samples):
            arr = np.loadtxt(filename, delimiter=",", skiprows=1 + i * self.N_s, max_rows=self.N_s, dtype=np.float64)
            self.N.append(arr)