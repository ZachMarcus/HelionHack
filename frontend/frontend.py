#
# back end
#
import requests
import mysql.connector
import os
from scipy.cluster.vq import kmeans2, whiten

x_app_token = "WufOy5JwfKNPI1xmcQrK51bUb"
url_building_permits = "https://data.cityofboston.gov/resource/hfgw-p5wb.json"
request_building_permits = requests.get(url_building_permits, 
        headers={"X-App-Token":x_app_token})

###KMEANS###
coordinates = []
for e in request_building_permits.json():
    try:
        coordinates.append(e['location']['coordinates'])
    except:
        pass
centroids, labels = kmeans2(whiten(coordinates), 6, iter = 20)
norm_labels = [float(i)/max(labels) for i in labels]
###KMEANS###

contents = ''
###FORMAT DATA FOR OUTPUT###
for i in range(0, max(labels)):
    output = ''
    for j in range(0, len(norm_labels)):
        if labels[j] == i:
            new = str(coordinates[j][0]) + ':' + str(coordinates[j][1]) + ':' + \
            str(norm_labels[j]) + ";"
            output += new
    contents += output
    
#
# Front end
#
import os
import sys
from bottle import route, view, run, template, static_file

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/')
@view('index')
def index():
    return {'contents': contents } 

run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
