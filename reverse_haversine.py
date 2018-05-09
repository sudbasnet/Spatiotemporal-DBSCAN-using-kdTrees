from haversine import haversine

def reverse_haversine(point, d, miles = False):
    lat1, lng1 = point
    lng2 = lng1
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin((lat2 - lat1) * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

    sin(lat2/2) cos(lat1/2) - cos(lat2/2) sin(lat1/2)

    z (x sinA - y cosA)

