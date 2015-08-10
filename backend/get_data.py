"""This contains the code to get the data and pass it to the SQL
Database"""

import requests
import mysql.connector

x_app_token = "WufOy5JwfKNPI1xmcQrK51bUb"

url_building_permits = "https://data.cityofboston.gov/resource/hfgw-p5wb.json"

request_building_permits = requests.get(url_building_permits, 
        headers={"X-App-Token":x_app_token})

print(request_building_permits.json()[0])

conn = MySQLdb.connect(host="localhost", 
                    user="test", 
                    passwd="test", 
                    db="hphackday")

cur = conn.cursor()

# Create Building Permit Table
cur.execute('CREATE TABLE IF NOT EXISTS '\
	'BUILDING_PERMITS(zip, description, city, state, status, '\
        'location, coordinates, owner, issued_date, applicant, '\
        'property_id, address, sq_feet, comments, parcel_id, '\
        'permit_number, occupancytype, permittypedesc, '\
        'expiration_date, declared_valuation, total_fees, worktype)')

for e in request_building_permits.json():
    # Insert JSON data into building permit table
    cur.execute('INSERT OR IGNORE INTO BUILDING_PERMITS '\
	        'VALUES(, %d, \'%s\', \'%s\', %d, %d, %d, %d, \'%s\', '\
                '%d, %d, \'%s\', %d, %d, %d, %d);'
                % (e['zip'], e['description'], e['city'], e['state'], e['status'],
                e['location'], e['coordinates'], e['owner'], e['issued_date'],
                e['applicant'], e['property_id'], e['address'], e['sq_feet'], 
                e['comments'], e['parcel_id'], e['permit_number'], e['occupancy'], 
                e['permittypedesc'], e['expiration_date'],
                e['declared_valuation'], e['total_fees'], e['worktype']))

#cur.execute('CREATE TABLE IF NOT EXISTS '\
#            'BUILDING_PERMITS(centroid, values)')

#cur.execute('INSERT OR IGNORE INTO BUILDING_PERMITS '\
#            'VALUES(%d, %s);' % (centroid, value_string))





