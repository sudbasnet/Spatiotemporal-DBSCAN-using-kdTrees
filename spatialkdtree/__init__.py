from spatialkdtree.Node import Node
import math
import copy
import pandas
from collections import deque
import fileinput
from haversine import haversine, AVG_EARTH_RADIUS
from datetime import datetime, timedelta


# Our comparator
# this is used for sorting the data frame
def float_compare(x, y):
    if x > y:
        return 1
    elif x == y:
        return 0
    else:
        return -1


# Generate our KDTree.  Depth starts at 0 and gets incremented as we recurse
def generate(points, tree_depth=0):
    if points == []:
        return None
    # This is either 0, 1 or 2 since we are using a 3 dimensional space
    axis = tree_depth % 3 + 1
    # Sort the points by their coordinates
    p = sorted(points, key=lambda x: float(x[axis]), reverse=False)
    # Pick the middle point of the tree to start as the root.
    median = int(math.floor(len(p) / 2))
    # Set this node to the first value
    node = Node(p[median][0], p[median][1:3], p[median][3], axis - 1,  None, None)
    # Generate the left side of the tree.
    node.left = generate(p[0:median], tree_depth + 1)
    # Generate the right side of the tree.
    node.right = generate(p[median+1:], tree_depth + 1)
    return node


# This function gives us a new tree starting from any node passed as n out of the tree
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


# Here we define a function that will return a (lon,lat) coordinate based
# on the source-point, distance (in km) and the bearing degree (0 or 90 or 180 or 270)
def get_coordinate(point, d, bearing=0):
    global AVG_EARTH_RADIUS  # Radius of the Earth in km, pulled from haversine package
    radius = AVG_EARTH_RADIUS
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
    delta_t = timedelta(days=distance_tuple[1])  # time difference
    cross_bounding = [[point, None]]
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
    boundingbox.update({"max": (x_max, y_max, t_max)})
    boundingbox.update({"min": (x_min, y_min, t_min)})
    return boundingbox


# returns true if a point (x,y,z) is within a boundingbox returned from get_bbox()
def is_valid(xyz, boundingbox):
    boundingbox_max = boundingbox["max"]
    boundingbox_min = boundingbox["min"]
    if boundingbox_min[0] <= xyz[0] <= boundingbox_max[0] and boundingbox_min[1] <= xyz[1] <= boundingbox_max[1] and \
            boundingbox_min[2] <= xyz[2] <= boundingbox_max[2]:
        return True
    return False


# now we read this bounding coordinates to traverse the dataset
# the original tree has been passed, with the current node and bounding coordinates
def fixed_radius_neighbors(tree, input_node, distance):
    boundingbox = get_bbox(input_node, distance)
    boundingbox_max = boundingbox["max"]
    boundingbox_min = boundingbox["min"]
    neighbors = []
    node_path = deque([tree])
    lon1, lat1 = input_node.coords
    while len(node_path) > 0:
        current_node = node_path.popleft()
        lon2, lat2 = current_node.coords
        xyz = (current_node.coords[0], current_node.coords[1], current_node.day)
        if is_valid(xyz, boundingbox):
            if haversine((lat1, lon1), (lat2, lon2)) <= distance[0] and current_node.id != input_node.id:
                neighbor = Node(id=current_node.id, coords=current_node.coords, day=current_node.day)
                neighbors.append(neighbor)
        axis = current_node.axis
        if boundingbox_max[axis] > xyz[axis] and boundingbox_min[axis] > xyz[axis] and current_node.hasRight():
            node_path.append(current_node.right)
        elif boundingbox_max[axis] < xyz[axis] and boundingbox_min[axis] < xyz[axis] and current_node.hasLeft():
            node_path.append(current_node.left)
        elif boundingbox_max[axis] >= xyz[axis] >= boundingbox_min[axis]:
            if current_node.hasRight():
                node_path.append(current_node.right)
            if current_node.hasLeft():
                node_path.append(current_node.left)
    return neighbors


def import_data(file, sep):
    df = pandas.read_csv(file, sep=sep)
    return df


# reading a file, where the first 4 columns are:
# id, longitude, latitude, date in YYYYMMDD format
def prep_dataset(df):
    points = []
    for index, row in df.iterrows():
        points.append((int(row[0]), float(row[1]), float(row[2]), int(row[3])))
        # these points are all numeric so they could be sorted faster
        # if date contains time, use YYYYMMDDHHMMSS (they should be capable of numeric sorting)
    return points


def get_frnn(dataset, tree, dist):
    events_frnn = {}
    count = 0
    for i in dataset:
        count +=1
        nn_array = []
        n = Node(i[0], (i[1], i[2]), i[3])
        # print("check it: ", i[0], (i[1], i[2]), i[3])
        frnn_nbrs = fixed_radius_neighbors(tree, n, dist)
        for nbr in frnn_nbrs:
            nn_array.append(nbr.id)
        events_frnn.update({n.id: nn_array})
        if count % 500 == 0:
            print(count, " events processed.")
    return events_frnn
