from utils import *
from writer import outputWriter
import reader
import numpy as np 

def testReader():
    print('testing readers...')
    bodyA = reader.BodyLEDs("Problem5-BodyA.txt") 
    bodyB = reader.BodyLEDs("Problem5-BodyB.txt") 
    mesh = reader.SurfaceMesh("Problem5MeshFile.sur") 
    sample_readings = reader.SampleReadings("PA5-A-Debug-SampleReadingsTest.txt")
    atlas_modes = reader.AtlasModes("Problem5Modes.txt")
    assert (bodyA.N_markers == 6)
    assert (bodyB.N_markers == 6)
    assert mesh.N_vertices == 1568
    assert mesh.N_triangles == 3135
    assert sample_readings.N_s == 16
    assert sample_readings.N_samples == 150
    assert sample_readings.N_modes == 6
    assert atlas_modes.Nvertices == 1568
    assert atlas_modes.Nmodes == 6
    assert atlas_modes.data[0][0][0] == -23.79
    assert atlas_modes.data[0][atlas_modes.Nvertices - 1][0] == 18.91
    mode_6 = atlas_modes.data[6]
    assert mode_6[atlas_modes.Nvertices - 1][0] == 0.02
    assert mode_6[atlas_modes.Nvertices - 1][1] == 0.01
    assert mode_6[atlas_modes.Nvertices - 1][2] == 0

def testFindLambdas():
    atlas_modes = reader.AtlasModes("Problem5Modes.txt")
    mesh = reader.SurfaceMesh("Problem5MeshFile.sur") 
    
    c_k, tri_k = testClosestPointMesh()
    #result = find_lambdas(c_k, tri_k, atlas_modes,c_k, mesh)
    #print(result)

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
    #outputWriter(3, "test.txt", A, B, vals)

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
    mesh = reader.SurfaceMesh("Problem5MeshFile.sur") 
    x = np.array([15.22, -34.6, 4.2])
    return FindClosestPointMesh(x, mesh.verts, mesh.tris)
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
    # print(center)
    # print(radius)

def testBarycentric():
    verts = [] 
    verts.append(np.array([252.49, 49.4, 121.5]))
    verts.append(np.array([100.0, 3.9, 210.59]))
    verts.append(np.array([43.5, 60.1, 4.3]))

    # print('vertices of triangle are: ')
    # print(verts[0])
    # print(verts[1])
    # print(verts[2])

    pt = np.array([125.9, 35.1, 99.4])

    # print('desired point is: ')
    # print(pt)

    u,v,w = barycentric(verts, pt)

    #print('results:')
    # print(u*verts[0])
    # print(v*verts[1])
    # print(w*verts[2])

    potential = u*verts[0] + v*verts[1] + w*verts[2]
    # print(potential)
    # assert potential[0] == pt[0] 
    # assert potential[1] == pt[1] 
    # assert potential[2] == pt[2] 

if __name__ == "__main__":
    testReader()
    testWriter()
    testClosestPointTri()
    testClosestPointMesh()
    testBoundingSphere()
    testBarycentric()
    testFindLambdas()
    print("All tests passed!")