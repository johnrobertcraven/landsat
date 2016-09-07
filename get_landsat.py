import urllib
import os


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
#TO DO
"""
Get scene list from AWS
-For a given input scene, print to screen which scenes are available
-Prompt selection of scenes
-Download to folder
"""

#
tmp_imgname, tmp_url  = build_url()

#Get image from Amazon S3 bucket
urllib.urlretrieve(tmp_url+tmp_imgname, tmp_imgname)


