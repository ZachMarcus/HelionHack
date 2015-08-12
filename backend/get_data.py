"""This contains the code to get the data and pass it to the SQL
Database"""

import requests
import mysql.connector
import os
import urllib.parse
from scipy.cluster.vq import kmeans2, whiten


# Global Variables
# This App Token is used for the SODA2 Database
x_app_token = "WufOy5JwfKNPI1xmcQrK51bUb"
url_building_permits = "https://data.cityofboston.gov/resource/hfgw-p5wb.json"


def getDbInfo():
    """This function parses the DATABASE_URL cloud environment variable
    to get the MySQL database information
    Returns 4 strings containing the info    
    """
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
    db_host = db_info['default']['HOST']
    db_password = db_info['default']['PASSWORD']
    #db_port = db_info['default']['PORT']
    return db_host, db_name, db_user, db_password

def getMySQLConnection(db_host, db_name, db_user, db_password):
    conn = mysql.connector.connect(user=db_user,
                               password=db_password,
                               host=db_host,
                               database=db_name)
    cur = conn.cursor()   
    return cur

def getCoordinates(json_list)
    """Parse JSON data and return a list of lists containing
    lat long pairs
    """
    coordinates = []
    for e in json_list:
        try:
            coordinates.append(e['location']['coordinates'])
        except:
            pass
    return coordinates
    
def KmeansLocationData(coordinates):
    """Performs KMeans clustering on latitude and longitude coordinates
    Returns the centroids, labels, and a list of normalized
    labels
    """
    centroids, labels = kmeans2(whiten(coordinates), 6, iter = 20)
    norm_labels = [float(i)/max(labels) for i in labels]
    return centroids, labels, norm_labels
    
def OutputLocationAsString(labels, norm_labels, coordinates)
    """Takes the coordinate and KMeans output and outputs all the locations
    in one long string.
    The form is lat:long:norm_value;
    THIS FUNCTION IS ONLY USED FOR TESTING
    """
    location_string = ''
    for i in range(0, max(labels)):
        output = ''
        for j in range(0, len(norm_labels)):
            if labels[j] == i:
                new = str(coordinates[j][0]) + ':' + str(coordinates[j][1]) + ':' + \
                str(norm_labels[j]) + ";"
                output += new
    location_string += output
    return location_string
    
def ProcessBuildingPermits(cur):
    """This function parses the building permit data and adds it to the 
    MySQL Database.
    """
    # Get the url request
    request_building_permits = requests.get(url_building_permits, 
        headers={"X-App-Token":x_app_token})
    
    # Get the list of coordinate pairs
    coordinates = getCoordinates(request_building_permits.json())
    
    # Run KMeans on the Location Data
    centroid, labels, norm_labels = KmeansLocationData(coordinates)
    
    # Create building permit table
    cur.execute('CREATE TABLE IF NOT EXISTS '\
            'BUILDING_PERMITS(centroid, values)')

    # Format Data for output and add to SQL Database
    for i in range(0, max(labels)):
        output = ''
        for j in range(0, len(norm_labels)):
            if labels[j] == i:
                new = str(coordinates[j][0]) + ':' + \
                      str(coordinates[j][1]) + ':' + \
                      str(norm_labels[j]) + ";"
                output += new
        # Add data to table
        cur.execute('INSERT OR IGNORE INTO BUILDING_PERMITS '\
                'VALUES(%d, %s);' % (i, output)
    
def main():
    """Main function
    """
    # Get MySQL DB Info
    db_host, db_name, db_user, db_password = getDbInfo()
    
    # Get mySQL Connection
    cur = getMySQLConnection(db_host, db_name, db_user, db_password)
    
    # Get Building Permit data and add to database
    ProcessBuildingPermits(cur)
    return 0

if __name__ = '__main__':
    main()







