import math
import copy
from collections import deque
import fileinput
from haversine import haversine
from datetime import datetime, timedelta

__author__ = 'Sudeep Basnet'


# def circle_distance(node, target, miles=False):
#     p1 = (node.coords[0], node.coords[1])
#     p2 = (target[0], target[1])
#     return haversine.haversine(p1, p2, miles)


def time_distance(node, target):
    return abs(node.t[2] - target[2])


# This represents our node.  Each node has a coordinate and a left and right node
class Node:
    def __init__(self, id, coords, day, left=None, right=None):
        self.id = id
        self.coords = coords
        self.day = day
        self.left = left
        self.right = right

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


# Our comparator
def float_compare(x,y):
    if x > y:
        return 1
    elif x == y:
        return 0
    else:
        return -1


def prep(file):
    points = []
    for line in fileinput.input(file):
        info = line.split(',')
        points.append((int(info[0]), float(info[1]), float(info[2]), int(info[3])))
        # print((int(info[0]), float(info[1]), float(info[2]), int(info[3])))
    return points


# Generate our KDTree.  Depth starts at 0 and gets incremented as we recurse
def generate(points, tree_depth=0):
    if points == []:
        return None
    # This is either 0, 1 or 2 since we are using a 3 dimensional space
    axis = tree_depth % 3 + 1
    # Sort the points by their coordinates
    p = sorted(points, key=lambda x: float(x[axis]), reverse=False)
    # Pick the middle point of the tree to start as the root.
    median = math.floor(len(p) / 2)
    # Set this node to the first value
    node = Node(p[median][0], p[median][1:3], p[median][3], None, None)
    # Generate the left side of the tree.
    node.left = generate(p[0:median], tree_depth + 1)
    # Generate the right side of the tree.
    node.right = generate(p[median+1:], tree_depth + 1)
    return node


def get_subtree(tree, n, tree_depth=0):
    if tree.id == n.id:
        return tree
    axis = tree_depth % 3
    tree_val = 0
    node_val = 0
    next_node = copy.deepcopy(tree)
    if axis < 2:
        tree_val = tree.coords[axis]
        node_val = n.coords[axis]
    elif axis == 2:
        tree_val = tree.day
        node_val = n.day
    if node_val < tree_val:
        next_node = tree.left
    elif node_val > tree_val:
        next_node = tree.right
    return get_subtree(next_node, n, tree_depth+1)


# def get_all_side_nodes(kdtree_item, side='all'):
#     q = queue.Queue()
#     side_nodes = []
#     if side == 'l':
#         q.put(kdtree_item.left)
#     elif side == 'r':
#         q.put(kdtree_item.right)
#     else:
#         q.put(kdtree_item.left)
#         q.put(kdtree_item.right)
#     while not q.empty():
#         n = q.get()
#         side_nodes.append(n.id)
#         if n.left is not None:
#             q.put(n.left)
#         if n.right is not None:
#             q.put(n.right)
#     return side_nodes


# Here we define a function that will return a (lon,lat) coordinate based
# on the source-point, distance (in km) and the bearing degree (0 or 90 or 180 or 270)
def get_coordinate(point, d, bearing=0):
    radius = 6378.1  # Radius of the Earth in km
    lon1, lat1 = point
    lon1, lat1, bearing = map(math.radians, [lon1, lat1, bearing])
    lat2 = math.asin(math.sin(lat1) * math.cos(d / radius) + math.cos(lat1) * math.sin(d / radius) * math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(d / radius) * math.cos(lat1), math.cos(d / radius) -
                             math.sin(lat1) * math.sin(lat2))
    lon2, lat2 = map(math.degrees, [lon2, lat2])
    point2 = (lon2, lat2)
    return point2


# Now we use the above function to get a bounding box
# around our source point. distance_tuple = (spatial_distance, temporal_distance)
def get_bbox(node, distance_tuple, bearing=0):
    point = node.coords
    t = datetime.strptime(str(node.day), '%Y%m%d')
    d = distance_tuple[0]
    delta_t = timedelta(days=distance_tuple[1])
    cross_bounding = [[point, None]]
    bounding = []
    boundingbox = {}
    x_max = point[0]
    x_min = point[0]
    y_max = point[1]
    y_min = point[1]
    for x in range(4):  # 4 different directions
        point2 = [get_coordinate(point, d, bearing), bearing]
        cross_bounding.append(point2)
        if x_max < point2[0][0]:
            x_max = point2[0][0]
        if x_min > point2[0][0]:
            x_min = point2[0][0]
        if y_max < point2[0][1]:
            y_max = point2[0][1]
        if y_min > point2[0][1]:
            y_min = point2[0][1]
            # starting at 0 degrees, we add 90 degree until we get points in all 4 directions
        bearing = bearing + 90
    t_min = int(datetime.strftime(t - delta_t, '%Y%m%d'))
    t_max = int(datetime.strftime(t + delta_t, '%Y%m%d'))
    bb_left_above = (x_min, y_max)
    bounding.append(bb_left_above)
    bb_left_down = (x_min, y_min)
    bounding.append(bb_left_down)
    bb_right_above = (x_max, y_max)
    bounding.append(bb_right_above)
    bb_right_below = (x_max, y_min)
    bounding.append(bb_right_below)
    boundingbox.update({"max": (x_max, y_max, t_max)})
    boundingbox.update({"min": (x_min, y_min, t_min)})
    return boundingbox


def is_valid(xyz, boundingbox):
    boundingbox_max = boundingbox["max"]
    boundingbox_min = boundingbox["min"]
    if boundingbox_min[0] <= xyz[0] <= boundingbox_max[0] and boundingbox_min[1] <= xyz[1] <= boundingbox_max[1] and \
            boundingbox_min[2] <= xyz[2] <= boundingbox_max[2]:
        return True
    else:
        return False


# now we read this bounding coordinates to traverse the dataset
# the original tree has been passed, with the current node and bounding coordinates
def fixed_radius_neighbors(tree, input_node, distance):
    tree_depth = 0
    boundingbox = get_bbox(input_node, distance)
    boundingbox_max = boundingbox["max"]
    boundingbox_min = boundingbox["min"]
    neighbors = []
    node_path = deque([tree])
    while len(node_path) > 0:
        current_node = node_path.popleft()
        # print("selfid: ", current_node.id)
        xyz = (current_node.coords[0], current_node.coords[1], current_node.day)
        if is_valid(xyz, boundingbox):
            if haversine(current_node.coords, input_node.coords) <= distance[0] and current_node.id != input_node.id:
                neighbor = Node(id=current_node.id, coords=current_node.coords, day=current_node.day)
                neighbors.append(neighbor)
        axis = tree_depth % 3
        if boundingbox_max[axis] > xyz[axis] and boundingbox_min[axis] >= xyz[axis] and current_node.hasRight():
            # print("Adding right")
            node_path.append(current_node.right)
        elif boundingbox_max[axis] <= xyz[axis] and boundingbox_min[axis] < xyz[axis] and current_node.hasLeft():
            # print("Adding Left")
            node_path.append(current_node.left)
        elif boundingbox_max[axis] > xyz[axis] > boundingbox_min[axis]:
            # print("Adding both")
            if current_node.hasRight():
                node_path.append(current_node.right)
            if current_node.hasLeft():
                node_path.append(current_node.left)
        tree_depth = tree_depth + 1
    return neighbors
