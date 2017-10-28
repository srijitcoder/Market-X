'''
Angular radius of query circle = r
Radius of Earth = R (kilometers)
Circle that is formed by all points which have distance d (kilometers) from M the query circle
Then, r = d/R
#Computing the Minimum and Maximum Latitude
   Let, M=(lat, lon)
  lat_min = lat - r rad 
  lat_max = lat + r rad

# Computing the Minimum and Maximum Longitude
	latT = arcsin(sin(lat)/cos(r))
	lon_min = lonT1 = lon - delta(lon)
	lon_max = lonT2 = lon + delta(lon)
	delta(lon) = arccos( ( cos(r) - sin(latT) * sin(lat) ) / ( cos(latT) * cos(lat) ) ) = arcsin(sin(r)/cos(lat))
# Poles and the 180th Meridian
	#TODO
# Optimized SQL Query 
	SELECT * FROM Places WHERE
    (Lat => lat_min AND Lat <= lat_max) AND (Lon >= lon_min AND Lon <= lon_max)
	AND
    acos(sin(lat) * sin(Lat) + cos(lat) * cos(Lat) * cos(Lon - (lon))) <= r;
***********************************************************************************************
Source : http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates#SQLQueries
**********************************************************************************************
'''

import math
import numpy as np
RADIUS_EARTH = 6371.0

class Geolocation:

	def __init__(self,lat,lon,distance):

		self.lat = lat  # in radians
		self.lon = lon # in radians
		self.distance = float(distance) # in kilometers



	def angular_radius(self):

		return float(self.distance/RADIUS_EARTH) 


	def min_max_latitudes(self):
		
		lat_min = self.lat - self.angular_radius() 
		lat_max = self.lat + self.angular_radius()

		return (lat_min,lat_max)

	def min_max_longitudes(self):

		r = self.angular_radius()

		latT = np.arcsin(math.sin(self.lat)/math.cos(r))
		
		delta_lon = np.arccos( ( math.cos(r) - math.sin(latT) * math.sin(self.lat) ) / ( math.cos(latT) * math.cos(self.lat) ) )
		
		lon_min =  self.lon - delta_lon
		lon_max =  self.lon + delta_lon

		return (lon_min,lon_max)

