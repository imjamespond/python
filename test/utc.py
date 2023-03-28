
import datetime

datestr = "2023-03-02T04:43:25,000000+00:00"
datestr = datestr.split(',', 1 )
dt = datetime.datetime.strptime(datestr[0],"%Y-%m-%dT%H:%M:%S")

print(dt)