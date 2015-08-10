"""This contains the code to get the data and pass it to the SQL
Database"""

import requests
import MySQLdb

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

cur.execute('CREATE TABLE IF NOT EXISTS '\
	'BUILDING_PERMITS(zip, description, city, state, status, '\
        'location, coordinates, owner, issued_date, applicant, '\
        'property_id, address, sq_feet, comments, parcel_id, '\
        'permit_number, occupancytype, permittypedesc, '\
        'expiration_date, declared_valuation, total_fees, worktype)')

#cur.execute('




