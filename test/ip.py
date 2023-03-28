import os
import geoip2.database 

try:

    file = os.getenv('HOME')+"/Downloads/Country.mmdb"
    with geoip2.database.Reader(file) as reader:
        response = reader.country("46.101.140.131")
        print(response.country)  

except BaseException as err: 
    print(err)

file = os.getenv('HOME')+"/Downloads/GeoLite2-City.mmdb"
with geoip2.database.Reader(file) as reader: 
    response = reader.city("46.101.140.131")
    print(response.city) 