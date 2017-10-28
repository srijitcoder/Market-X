#TODO
from geopy.distance import great_circle


def getDistance(lat1,lon1,lat2,lon2):
    first = (lat1,lon1)
    second = (lat2,lon2)

    distance = (great_circle(first,second).miles)
    print (distance)
    return distance
getDistance(41.49008, -71.312796,41.499498, -81.695391)




'''According to Wikipedia, Vincenty's formula is slower but more accurate.....
    To conclude: Vincenty's formula is doubles the calculation time compared to great-circle, and its accuracy
    gain at the point tested is ~0.17%.
    https://gis.stackexchange.com/questions/84885/whats-the-difference-between-vincenty-and-great-circle-distance-calculations
'''

