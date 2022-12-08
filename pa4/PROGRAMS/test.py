from IterativeClosestPoint import FindClosestPointTri
from IterativeClosestPoint import FindClosestPointMesh
from IterativeClosestPoint import BoundingSphere
from writer import outputWriter
import reader
import numpy as np 
import unittest

def testReader():
    print('testing readers...')
    bodyA = reader.BodyLEDs("Problem4-BodyA.txt") 
    bodyB = reader.BodyLEDs("Problem4-BodyB.txt") 
    mesh = reader.SurfaceMesh("Problem4MeshFile.sur") 
    sample_readings = reader.SampleReadings("PA4-A-Debug-SampleReadingsTest.txt")
    assert (bodyA.N_markers == 6)
    assert (bodyB.N_markers == 6)
    assert mesh.N_vertices == 1568
    assert mesh.N_triangles == 3135
    assert sample_readings.N_s == 16
    assert sample_readings.N_samples == 75

def testWriter():
    print('testing writers...')
    A = []
    B = []
    vals = [] 
    A.append(np.array([43563.123, 1250.456, -154.6]))
    A.append(np.array([649.10, -345.123987, -5189.1123]))
    A.append(np.array([4529.2, -2487, 1481.52]))

    B.append(np.array([-235.35, 582.15, -59812.5]))
    B.append(np.array([146.3, 405.1, -3894.5915]))
    B.append(np.array([6391.5, -49145.1, 549.21]))

    vals.append(50)
    vals.append(514)
    vals.append(531)
    outputWriter(3, "test.txt", A, B, vals)

def testClosestPointTri():
    print('testing FindClosestPointTri...')
    A = []
    A.append(np.array([0,0,0]))
    A.append(np.array([0,1,0]))
    A.append(np.array([1,0,0]))

    x = np.array([1,1,0])

    c = FindClosestPointTri(x, A)
    assert (c[0] == 0.5)
    assert (c[1] == 0.5)
    assert (c[2] == 0)

def testClosestPointMesh():
    print('testing FindClosestPointMesh...')
    mesh = reader.SurfaceMesh("Problem3MeshFile.sur") 
    x = np.array([15.22, -34.6, 4.2])
    c, tri = FindClosestPointMesh(x, mesh.verts, mesh.tris)
    # print(c)
    # print(mesh.verts[tri[0]])
    # print(mesh.verts[tri[1]])
    # print(mesh.verts[tri[2]])

def testBoundingSphere():
    print('Testing BoundingSphere...')
    A = []
    A.append(np.array([1,1,1]))
    A.append(np.array([2,2,2]))
    A.append(np.array([3,3,3]))

    center, radius = BoundingSphere(A)
    print(center)
    print(radius)

if __name__ == "__main__":
    #testReader()
    # testWriter()
    # testClosestPointTri()
    # testClosestPointMesh()
    testBoundingSphere()
    print("All tests passed!")