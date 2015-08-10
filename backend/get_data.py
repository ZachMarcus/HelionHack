"""This contains the code to get the data and pass it to the SQL
Database"""

import requests

x_app_token = "WufOy5JwfKNPI1xmcQrK51bUb"
building_permits_url = "https://data.cityofboston.gov/resource/hfgw-p5wb.json"

r = requests.get(building_permits_url, 
        headers={"X-App-Token":x_app_token})

r.json()[0]

