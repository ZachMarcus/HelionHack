"""This contains the code to get the data and pass it to the SQL
Database"""

import requests
import mysql.connector
import os
import urlparse
from scipy.cluster.vq import kmeans2, whiten
from bottle import run

# Global Variables
# This App Token is used for the SODA2 Database
x_app_token = "f85FHSBu3N8hFk2F6cRbnpC4O"
url_building_permits = "https://data.cityofboston.gov/resource/msk6-43c6.json"

def getDbInfo():
    """This function parses the DATABASE_URL cloud environment variable
    to get the MySQL database information
    Returns 4 strings containing the info    
    """
    DATABASE_URL = os.environ['DATABASE_URL']
    db_info = {}
    url = urlparse.urlparse(DATABASE_URL)
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
    print 'host = ' + db_host
    print 'name = ' + db_name
    print 'user = ' + db_user
    print 'passwrd = ' + db_password
   
    return db_host, db_name, db_user, db_password

def getMySQLConnection(db_host, db_name, db_user, db_password):
    global conn
    conn = mysql.connector.connect(user=db_user,
                               password=db_password,
                               host=db_host,
                               database=db_name)
    cur = conn.cursor()   
    return cur

def getCoordinates(json_list):
    """Parse JSON data and return a list of lists containing
    lat long pairs
    """
    coordinates = []
    for e in json_list:
        inner_list = []
        try:
            inner_list.append(float(e['location']['latitude']))
            inner_list.append(float(e['location']['longitude']))
            coordinates.append(inner_list)
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
    
def OutputLocationAsString(labels, norm_labels, coordinates):
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
    centroids, labels, norm_labels = KmeansLocationData(coordinates)
    
    # Create building permit table
    cur.execute("""CREATE TABLE IF NOT EXISTS BUILDING_PERMITS (
            centroids INT,
            vals VARCHAR(10000))""")
    
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
        add_centroid = ("INSERT INTO BUILDING_PERMITS "
                        "(centroids, vals) "
                        "VALUES (%s, %s)")
        data_centroid = (i, output)
        cur.execute(add_centroid, data_centroid)


        #cur.execute("""
        #        INSERT INTO BUILDING_PERMITS (centroids, vals)
        #        VALUES 
        #            (%s, %s)
        #        """, (i, output))
        conn.commit()
    
def main():
    """Main function
    """
    # Get MySQL DB Info
    db_host, db_name, db_user, db_password = getDbInfo()
    
    # Get mySQL Connection
    cur = getMySQLConnection(db_host, db_name, db_user, db_password)
    
    # Get Building Permit data and add to database
    ProcessBuildingPermits(cur)

    cur.close()
    conn.close()



if __name__ == '__main__':
    run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
    main()








