from __future__ import print_function
import numpy as np

class Node(object):
    """
    An OctNode
    """
    def __init__(self, pos, _size, _depth, _data):
        self.position = pos
        self.size = _size
        self.depth = _depth
        self.isLeafNode = True
        self.data = _data

        # branches is a list of 8 children
        self.branches = [None, None, None, None, None, None, None, None]

        ## The cube's bounding coordinates
        self.lower = (self.position[0] - self.size / 2, self.position[1] - self.size / 2, self.position[2] - self.size / 2)
        self.upper = (self.position[0] + self.size / 2, self.position[1] + self.size / 2, self.position[2] + self.size / 2)

class Octree(object):
    """
    wooo an octreeeee
    """
    def __init__(self, worldSize, origin=(0, 0, 0), max_type="nodes", max_value=10):

        self.root = Node(origin, worldSize, 0, [])
        self.worldSize = worldSize
        self.limit_nodes = (max_type=="nodes")
        self.limit = max_value

    @staticmethod
    def create(position, size, objects):
        """This creates the actual OctNode itself."""
        return Node(position, size, objects)

    def insert(self, position, objData=None):
        if np:
            if np.any(position < self.root.lower):
                return None
            if np.any(position > self.root.upper):
                return None
        else:
            if position < self.root.lower:
                return None
            if position > self.root.upper:
                return None

        if objData is None:
            objData = position

        return self.insert_(self.root, self.root.size, self.root, position, objData)

    def insert_(self, root, size, parent, position, objData):
        if root is None:
            pos = parent.position

            ## offset is halfway across the size allocated for this node

            ## find out which direction we're heading in
            branch = self.find_branch(parent, position)

            ## new center = parent position + (branch direction * offset)
            newCenter = (0, 0, 0)

            if branch == 0:
                newCenter = (pos[0]-size / 2, pos[1]-size / 2, pos[2]-size / 2 )
            elif branch == 1:
                newCenter = (pos[0]-size / 2, pos[1]-size / 2, pos[2]+size / 2 )
            elif branch == 2:
                newCenter = (pos[0]-size / 2, pos[1]+size / 2, pos[2]-size / 2 )
            elif branch == 3:
                newCenter = (pos[0]-size / 2, pos[1]+size / 2, pos[2]+size / 2 )
            elif branch == 4:
                newCenter = (pos[0]+size / 2, pos[1]-size / 2, pos[2]-size / 2 )
            elif branch == 5:
                newCenter = (pos[0]+size / 2, pos[1]-size / 2, pos[2]+size / 2 )
            elif branch == 6:
                newCenter = (pos[0]+size / 2, pos[1]+size / 2, pos[2]-size / 2 )
            elif branch == 7:
                newCenter = (pos[0]+size / 2, pos[1]+size / 2, pos[2]+size / 2 )

            return Node(newCenter, size, parent.depth + 1, [objData])

        #else: are we not at our position, but not at a leaf node either
        elif (
            not root.isLeafNode
            and
            (
                (np and np.any(root.position != position))
                or
                (root.position != position)
            )
        ):

            branch = self.__findBranch(root, position)
            newSize = root.size / 2
            root.branches[branch] = self.__insertNode(root.branches[branch], newSize, root, position, objData)

        elif root.isLeafNode:
            if (
                (self.limit_nodes and len(root.data) < self.limit)
                or
                (not self.limit_nodes and root.depth >= self.limit)
            ):
                root.data.append(objData)
            else:

                root.data.append(objData)
                objList = root.data
                root.data = None
                root.isLeafNode = False
                newSize = root.size / 2
                for ob in objList:
                    if hasattr(ob, "position"):
                        pos = ob.position
                    else:
                        pos = ob
                    branch = self.__findBranch(root, pos)
                    root.branches[branch] = self.__insertNode(root.branches[branch], newSize, root, pos, ob)
        return root

    def findPosition(self, position):
        if np:
            if np.any(position < self.root.lower):
                return None
            if np.any(position > self.root.upper):
                return None
        else:
            if position < self.root.lower:
                return None
            if position > self.root.upper:
                return None
        return self.find_position(self.root, position)

    @staticmethod
    def find_position(node, position, count=0, branch=0):
        """Private version of findPosition """
        if node.isLeafNode:
            return node.data
        branch = Octree.find_branch(node, position)
        child = node.branches[branch]
        if child is None:
            return None
        return Octree.find_position(child, position, count + 1, branch)

    @staticmethod
    def find_branch(root, position):
        """
        helper function
        returns an index corresponding to a branch
        pointing in the direction we want to go
        """
        index = 0
        if (position[0] >= root.position[0]):
            index |= 4
        if (position[1] >= root.position[1]):
            index |= 2
        if (position[2] >= root.position[2]):
            index |= 1
        return index

    def iterateDepthFirst(self):
        """Iterate through the octree depth-first"""
        gen = self.iterate_depth_first(self.root)
        for n in gen:
            yield n

    @staticmethod
    def iterate_depth_first(root):
        """Private (static) version of iterateDepthFirst"""

        for branch in root.branches:
            if branch is None:
                continue
            for n in Octree.iterate_depth_first(branch):
                yield n
            if branch.isLeafNode:
                yield branch
