# This represents our node.
# Each node has a uniqueid, coordinates (in degrees), axis (0,1,2 representing lon, lat, day), and a left and right node


class Node:
    def __init__(self, id, coords, day, axis=0, left=None, right=None):
        self.id = id
        self.coords = coords
        self.day = day
        self.left = left
        self.right = right
        self.axis = axis

    def isLeaf(self):
        if self.left is None and self.left is None:
            return True
        return False

    def hasLeft(self):
        if self.left is not None:
            return True
        return False

    def hasRight(self):
        if self.right is not None:
            return True
        return False

    def isNode(self):
        if self.hasLeft() and self.hasRight:
            return True
        return False
