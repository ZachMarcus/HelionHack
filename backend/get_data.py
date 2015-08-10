"""This contains the code to get the data and pass it to the SQL
Database"""

import requests
import mysql.connector
import os
import urllib.parse
from scipy.cluster.vq import vq, kmeans, whiten


##################  DB INFO
DATABASE_URL = os.getenv('DATABASE_URL')
db_info = {}
url = urllib.parse.urlparse(DATABASE_URL)
db_info['default'] = {
        'NAME': url.path[1:],
        'USER': url.username,
        'HOST': url.hostname,
        'PASSWORD': url.password,
        'PORT': url.port,
        }
db_name = db_info['default']['NAME']
db_user = db_info['default']['USER']
db_password = db_info['default']['PASSWORD']
db_port = db_info['default']['PORT']
#################### DB INFO


x_app_token = "WufOy5JwfKNPI1xmcQrK51bUb"

url_building_permits = "https://data.cityofboston.gov/resource/hfgw-p5wb.json"

request_building_permits = requests.get(url_building_permits, 
        headers={"X-App-Token":x_app_token})

conn = mysql.connector.connect(user=db_user,
                               password=db_password,
                               host=db_host,
                               database=db_name)

cur = conn.cursor()

# Create building permit table
cur.execute('CREATE TABLE IF NOT EXISTS '\
            'BUILDING_PERMITS(centroid, values)')

###KMEANS###
coordinates = []
for e in request_building_permits.json():
    try:
        locations.append(e['location']['coordinates'])
    except:
        pass
centroids, labels = kmeans2(whiten(coordinates), 6, iter = 20)
norm_labels = [float(i)/max(labels) for i in labels]
###KMEANS###

###FORMAT DATA FOR OUTPUT###
for i in range(0, max(labels)):
    output = ''
    for j in range(0, len(norm_labels)):
        if labels[j] == i:
            new = str(coordinates[j][0]) + ':' + str(coordinates[j][1]) + ':' + \
            str(norm_labels[j]) + ";"
            output += new
    
    # Add data to table
    cur.execute('INSERT OR IGNORE INTO BUILDING_PERMITS '\
                'VALUES(%d, %s);' % (i, output))





