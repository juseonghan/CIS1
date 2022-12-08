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
    # return the closest point and the indices of the triangle vertices 
    # tri_best_verts = np.array([verts[tri_best[0]], verts[tri_best[1]], verts[tri_best[2]]])
    return h, tri_best
    
def FindClosestPointMesh_Deformed(x, verts, tris, Lambdas, modes):

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
        # update the verts 

        # tri is one triangle which is a np array of verts. build A matrix
        A = []
        vert0 = verts[tri[0]]
        vert1 = verts[tri[1]]
        vert2 = verts[tri[2]]

        sum_s = np.zeros((3,1))
        sum_t = np.zeros((3,1))
        sum_u = np.zeros((3,1))

        # need to add in the deformation from Lambdas and mdoes
        for i in range(modes.Nmodes):
            modes_i = modes.data[i+1]
            ms = modes_i[tri[0]]
            mt = modes_i[tri[1]]
            mu = modes_i[tri[2]]
            sum_s = np.add(sum_s, Lambdas[i]*ms[...,None])
            sum_t = np.add(sum_t, Lambdas[i]*mt[...,None])
            sum_u = np.add(sum_u, Lambdas[i]*mu[...,None])
       
        vert0 = np.add(vert0, sum_s.reshape(3))
        vert1 = np.add(vert1, sum_t.reshape(3))
        vert2 = np.add(vert2, sum_u.reshape(3))

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
    # return the closest point and the indices of the triangle vertices 
    # tri_best_verts = np.array([verts[tri_best[0]], verts[tri_best[1]], verts[tri_best[2]]])
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
    """
    Custom dot product function
    """
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

def barycentric(verts, p):
    """
    Function to find the barycentric weights of p relative to the vertices of the triangle
    """

    # least squares approach
    a = verts[0][...,None]
    b = verts[1][...,None]
    c = verts[2][...,None]

    temp = np.hstack((a,b,c))
    X = np.vstack((temp, np.array([1,1,1])))

    y_temp = np.append(p, 1)
    y = y_temp[...,None]
    
    XTX = X.T @ X
    XTy = X.T @ y 

    # there exists a closed form solution for the weights in linear regression
    weights = np.linalg.inv(XTX) @ XTy 

    return weights.reshape(3)

def find_lambdas(c_k, tri_k, atlas_modes, s_k, mesh):
    """
    Function to find the lambdas, or the weights of the deformed barycentric centers
    input: the center point, triangle vertices, mode data, and the mesh data
    """
    # first find the weights
    verts_tri = []
    verts_tri.append(mesh.verts[tri_k[0]])
    verts_tri.append(mesh.verts[tri_k[1]])
    verts_tri.append(mesh.verts[tri_k[2]])
    bary_weights = barycentric(verts_tri, c_k)

    # now we need to find q
    q_k = []
    #q_k.append(c_k[...,None])
    for i in range(atlas_modes.Nmodes+1):
        q_mk = find_qmk(atlas_modes, tri_k, bary_weights, i)
        q_mk = q_mk[...,None]
        q_k.append(q_mk)

    # finally, solve the least squares problem to find the lambdas
    y = s_k - c_k[...,None]
    X = np.zeros((3, atlas_modes.Nmodes))

    for i in range(atlas_modes.Nmodes): 
        j = i + 1
        q_j = q_k[j]
        X[0, i] = q_j[0][0]
        X[1, i] = q_j[1][0]
        X[2, i] = q_j[2][0]

    # lambdas = (np.linalg.inv(XTX) @ XTy).T
    lambdas = np.linalg.lstsq(X, y, rcond=None)[0]
    lambdas = lambdas.reshape(atlas_modes.Nmodes)
    return lambdas.tolist(), q_k

def find_qmk(atlas_modes, tri_k, bary_weights, m):
    """
    Function to find q_mk, the barycentric coordinate of a point inside a triangle
    with variation 
    input: the mode data, triangle vertices, barycentric weights, and mode number 
    output: a list of vertices of the deformed vertex coordinates
    """
    atlas_i = atlas_modes.data[m]

    m_ms = atlas_i[tri_k[0]]
    m_mt = atlas_i[tri_k[1]]
    m_mu = atlas_i[tri_k[2]]

    result = bary_weights[0] * m_ms + bary_weights[1] * m_mt + bary_weights[2] * m_mu
    return result

def calculate_sk(lambdas, q_k, Nmodes):
    """
    Function to calculate new c_k values after calculating deformations
    input: deformation weights, q_k values, number of modes
    """
    sum = np.zeros((3,1))
    for i in range(Nmodes):
        sum = np.add(sum, lambdas[i] * q_k[i+1])
    return q_k[0] + sum