import heapq
import itertools
import operator
import math
from collections import deque
from functools import wraps
import fileinput
from haversine import haversine
from datetime import datetime
import copy
import queue

__author__ = 'Sudeep Basnet'

nearest = []
points = []
# has uniqueid, longitude, latitude and event date


def circle_distance(node, target, miles=False):
    p1 = (node.coords[0], node.coords[1])
    p2 = (target[0], target[1])
    return haversine.haversine(p1, p2, miles)


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


# Our comparator
def float_compare(x, y):
    if x > y:
        return 1
    elif x == y:
        return 0
    else:
        return -1


def prep(file):
    global points
    for line in fileinput.input(file):
        info = line.split(',')
        points.append((int(info[0]), float(info[1]), float(info[2]), int(info[3])))
        # print((int(info[0]), float(info[1]), float(info[2]), int(info[3])))
    root = generate(points)
    return root


# Generate our KDTree.  Depth starts at 0 and gets incremented as we recurse
def generate(points, tree_depth=0):
    if points==[]:
        return None
    # This is either 1 or 2 since we are using a 2 dimensional space
    axis = tree_depth % 3 + 1
    # Sort the points by their coordinates
    p = sorted(points, key=lambda x: float(x[axis]), reverse=False)
    # points.sort(cmp=lambda x,y: float_compare(x[axis], y[axis]))
    # Pick the middle point of the tree to start as the root.
    median = math.floor(len(p) / 2)
    # Set this node to the first value
    node = Node(p[median][0], p[median][1:3], p[median][3], None, None)
    # Generate the left side of the tree.
    node.left = generate(p[0:median], tree_depth + 1)
    # Generate the right side of the tree.
    node.right = generate(p[median+1:], tree_depth + 1)
    return node


def get_subtree(kdtree_item, n, tree_depth=0):
    if kdtree_item.id == n.id:
        return kdtree_item
    axis = tree_depth % 3
    maintree_val = 0
    node_val = 0
    nextnode = copy.deepcopy(kdtree_item)
    if axis < 2:
        maintree_val = kdtree_item.coords[axis]
        node_val = n.coords[axis]
    elif axis == 2:
        maintree_val = kdtree_item.day
        node_val = n.day
    if node_val < maintree_val:
        nextnode = kdtree_item.left
    elif node_val > maintree_val:
        nextnode = kdtree_item.right
    return get_subtree(nextnode, n, tree_depth+1)


def get_all_side_nodes(kdtree_item, side='all'):
    q = queue.Queue()
    side_nodes = []
    if side == 'l':
        q.put(kdtree_item.left)
    elif side == 'r':
        q.put(kdtree_item.right)
    else:
        q.put(kdtree_item.left)
        q.put(kdtree_item.right)
    while not q.empty():
        n = q.get()
        side_nodes.append(n.id)
        if n.left is not None:
            q.put(n.left)
        if n.right is not None:
            q.put(n.right)
    return side_nodes


kdTree_object = prep('events_data_write.csv')


# def nn(kd_tree, target, istreepoint = True ):
#     get_bbox(target)


def get_coordinate(point, d, bearing=0):
    R = 6378.1  # Radius of the Earth in km
    lon1, lat1 = point
    lon1, lat1, bearing = map(math.radians, [lon1, lat1, bearing])
    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) + math.cos(lat1) * math.sin(d / R) * math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(d / R) * math.cos(lat1), math.cos(d / R) - math.sin(lat1) * math.sin(lat2))
    lon2, lat2 = map(math.degrees, [lon2, lat2])
    point2 = (lon2, lat2)
    return point2


def get_bbox(point, d, bearing=0):
    cross_bounding = [[point, None]]
    bounding = []
    bounding_coords = {}
    x_max = point[0]
    x_min = point[0]
    y_max = point[1]
    y_min = point[1]
    for x in range(4):
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
        bearing = bearing + 90
    bb_left_above = (x_min, y_max)
    bounding.append(bb_left_above)
    bb_left_down = (x_min, y_min)
    bounding.append(bb_left_down)
    bb_right_above = (x_max, y_max)
    bounding.append(bb_right_above)
    bb_right_below = (x_max, y_min)
    bounding.append(bb_right_below)
    bounding_coords.update({"x_max": x_max})
    bounding_coords.update({"x_min": x_min})
    bounding_coords.update({"y_max": y_max})
    bounding_coords.update({"y_min": y_min})
    return bounding_coords


def find_neighbors(tree, input_node, distance):
    point = input_node.coords
    day = input_node.day
    bounding_coords = get_bbox(point, distance)
    x_max = bounding_coords['x_max']
    x_min = bounding_coords['x_min']
    y_max = bounding_coords['y_max']
    y_min = bounding_coords['y_min']
    tree_depth = 0
    




# def fixed_radius_neighbors(data, kdtree_of_data, eps, tree_depth=0):
#     return_set = {}
#     for i in range(len(data)+1):
#         neighbors = []
#         return_set.update({data[i][0] : []})
#         n = Node(data[i][0], (data[i][1], data[i][2]), data[i][3])
#         tree = get_subtree(kdTree_object, n)
#         left_subtree(tree, )
#         distance = (circle_distance(subtree, subtree.left) , time_distance())
#
#     thisnode = Node(data)
#     d =
#     axis = tree_depth % 3
#
#     maintree_val = 0
#     node_val = 0
#     nextnode = copy.deepcopy(kdtree_item)
#     if nextnode.id == n.id:
#         return nextnode
#     if axis < 2:
#         maintree_val = kdtree_item.coords[axis]
#         node_val = n.coords[axis]
#     elif axis == 2:
#         maintree_val = kdtree_item.day
#         node_val = n.day
#     if node_val < maintree_val:
#         nextnode = kdtree_item.left
#     elif n.node_val > maintree_val:
#         nextnode = kdtree_item.right
#     get_subtree(nextnode, n, tree_depth + 1)

