import urllib
import os
import pandas as pd
from geopy.distance import vincenty
import numpy as np

"""
Purpose: automate download of LandSat data from Amazon S3 Bucket

Overview of the AWS, and file path construction can be found here
Note: each band of a given scene is roughly 40 MB, be aware when downloading

Contact: johnrobertcraven at gmail
    https://aws.amazon.com/blogs/aws/start-using-landsat-on-aws/
    s3://landsat-pds/L8/003/017/LC80030172015001LGN00/
    LXSPPPRRRYYYYDDDGSIVV
    L = Landsat
    X = Sensor
    S = Satellite
    PPP = WRS path
    RRR = WRS row
    YYYY = Year
    DDD = Julian day of year
    GSI = Ground station identifier
    VV = Archive version number

#GZip file of all scenes
http://landsat-pds.s3.amazonaws.com/scene_list.gz
"""
def build_url(sat='LC',sens='8',spath='003', srow='017',yr='2014',
              ddd='270', gsi_vv='LGN00', band='B10'):
	"""
	Purpose: build a URL and image name, default values set from AMS example
	"""
	scene_img = sat+sens+spath+srow+yr+ddd+gsi_vv+'_'+band+'.TIF'
	scene_end = sat+sens+spath+srow+yr+ddd+gsi_vv
	scene_url = 'https://s3-us-west-2.amazonaws.com/landsat-pds/'+'L'+sens+'/'+spath+'/'+srow+'/'+scene_end+'/'

	return scene_img, scene_url

def latlong_to_wrs2(lat_in, long_in):
	
	tmp_site = (lat_in, long_in)
	
	#scene_list.csv contains path/row and location data for all scenes 
	locs = pd.read_csv('scene_list.csv')
	
	dist = np.zeros([locs.shape[0]])
	
	#Calculate distance from site to all scene centroids in miles
	for i in range(0,locs.shape[0]):
		scene_cent = (locs['lat_cent'].values[i],locs['long_cent'].values[i])
		dist[i] = vincenty(tmp_site, scene_cent).miles
	
	#get index - e.g. closest centroid to site
	idx = np.argmin(dist)
	wrs_path = locs['Path'].values[idx]
	wrs_row = locs['Row'].values[idx]
	
	#Check to get Day-time scene
	if lat_in > 0.:
		while wrs_path > 50:
			dist = np.delete(dist,idx)
			idx = np.argmin(dist)
			wrs_path = locs['Path'].values[idx]
			wrs_row = locs['Row'].values[idx]
		
	return wrs_path, wrs_row
#TO DO
"""
Get scene list from AWS
-For a given input scene, print to screen which scenes are available
-Prompt selection of scenes
-Download to folder
"""
#Near San Francisco
my_lat = 37.7
my_long = -122.5

my_path, my_row = latlong_to_wrs2(my_lat,my_long)

print my_path
print my_row 

#
#tmp_imgname, tmp_url  = build_url()

#Get image from Amazon S3 bucket
#urllib.urlretrieve(tmp_url+tmp_imgname, tmp_imgname)


