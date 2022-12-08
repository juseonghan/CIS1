import numpy as np 
from numpy import linalg
import sys 

def FindClosestPointMesh(x, verts, tris):

    """
    function to find the closest point to a mesh.
    verts is a list of vertices
    tris is the list of vertex indices that define the triangles
    """

    first_time = 1
    c_best = -1
    tri_best = 0

    for tri in tris:
        # tri is one triangle which is a np array of verts. build A matrix
        A = []
        vert0 = verts[tri[0]]
        vert1 = verts[tri[1]]
        vert2 = verts[tri[2]]
       
        A.append(vert0)
        A.append(vert1)
        A.append(vert2)

        # find the closest point to this triangle
        c_cur = FindClosestPointTri(x, A)

        if (first_time == 1):
            c_best = c_cur
            tri_best = tri 
            first_time = 0 
            continue 

        # if it's closer than the best, then update c_best
        if np.linalg.norm(x - c_cur) < np.linalg.norm(x - c_best):
            c_best = c_cur
            tri_best = tri 

    # at this point, c_best is the closest point to all triangles
    return c_best, tri_best

def FindClosestPointMesh_BS(x, verts, tris):

    """
    function to find the closest point to a mesh.
    verts is a list of vertices
    tris is the list of vertex indices that define the triangles
    """

    first_time = 1
    c_best = -1
    tri_best = 0
    bound = sys.maxsize 

    for tri in tris:
        # tri is one triangle which is a np array of verts. build A matrix
        A = []
        vert0 = verts[tri[0]]
        vert1 = verts[tri[1]]
        vert2 = verts[tri[2]]
       
        A.append(vert0)
        A.append(vert1)
        A.append(vert2)

        # first find the bounding sphere around this triangle
        center, radius = BoundingSphere(A)

        # see if this is worth checking
        if np.linalg.norm(vert1 - x) - radius < bound:
        

            # find the closest point to this triangle
            h = FindClosestPointTri(x, A)

            # change the bound
            temp = np.linalg.norm(h - x)
            if temp < bound:
                bound = temp

            if (first_time == 1):
                c_best = h
                tri_best = tri 
                first_time = 0 
                continue 

            # if it's closer than the best, then update c_best
            if temp < np.linalg.norm(x - c_best):
                c_best = h
                tri_best = tri 

    # at this point, c_best is the closest point to all triangles
    return h, tri_best
    
def FindClosestPointTri(x, A):

    """ 
    function to find the closest point to a triangle.
    A the list containing the three vertices of the triangle (P,Q,R)
    x the point we are registering
    """

    p = A[0].reshape(3,1)
    q = A[1].reshape(3,1)
    r = A[2].reshape(3,1)

    # set up the linear regression 
    x1 = (q - p)
    x2 = (r - p)

    X = np.hstack((x1,x2)) # 3 x 2 matrix 
    y = (x.reshape(3,1) - p) # 3 x 1 matrix

    XTX = X.T @ X # 2 x 2 matrix
    XTy = X.T @ y # 2 x 1 matrix

    # there exists a closed form solution for the weights in linear regression
    w = np.linalg.inv(XTX) @ XTy # 2 x 1 matrix, representing the weights 

    l = w[0]
    u = w[1] 

    c = p + l*(q-p) + u*(r-p) 
    
    # now test whether or not c is inside, outside, or along the border of A
    if l < 0:
        c = ProjectOnSegment(c,r,p)
    elif u < 0:
        c = ProjectOnSegment(c,p,q)
    elif l + u > 1:
        c = ProjectOnSegment(c,q,r)

    return c[:,0]

def ProjectOnSegment(pt, v1, v2):

    """
    function that projects a point to the line defined by v1, v2 
    """

    l = ( dot_prod((pt-v1), (v2-v1))) / ( dot_prod((v2-v1), (v2-v1)))
    temp = min([1, l])
    l_seg = max([0, temp])

    c_line = v1 + l_seg * (v2-v1)

    return c_line

def dot_prod(a,b):
    return a[0,0]*b[0,0] + a[1,0]*b[1,0] + a[2,0]*b[2,0]

def BoundingSphere(A):
    """
    Function to find the bounding sphere around a triangle with vertices given in A
    """
    a = A[0]
    b = A[1]
    c = A[2]

    f = (a+b)/2

    u = a - f 
    v = c - f

    temp = np.cross(u,v)
    d = np.cross(temp, u)

    if d[0] == 0 and d[1] == 0 and d[2] == 0:
        q = f
        p = np.linalg.norm(q-a) 
    else:
        y = (np.dot(v,v) - np.dot(u,u))/(np.dot(2*d, v-u))
        l = max(0, y)

        q = f + l * d # center
        p = np.linalg.norm(q-a) # radius

    return q, p