"""
from geopy import geocoders
from pytz import timezone
from datetime import datetime

g = geocoders.GoogleV3()
place, (lat, lng) = g.geocode("Singapore")
timezone = g.timezone((lat, lng))
format = '%Y-%m-%d %H:%M:%S %Z%z'

timezoneKA = timezone(str(timezone.)

standardLocation = timezoneKA.localize(datetime(2015, 12, 5, 14, 0, 0))
print(standardLocation.strftime(format))

print(place)
print(timezone)
"""

