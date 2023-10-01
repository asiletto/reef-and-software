from skyfield import api
from skyfield import almanac
from datetime import timedelta
import datetime
import pytz
from pytz import utc
import time

ts = api.load.timescale()
ephem = api.load_file('de421.bsp')

#https://en.wikipedia.org/wiki/List_of_reefs
CITY = {'lat': '-19.746975', 'lon': '149.207542', 'name':'Hardy Reef', 'elevation':0}

startTime = utc.localize(datetime.datetime.strptime('2023-10-01 12:00', '%Y-%m-%d %H:%M'))

t0 = ts.utc(startTime - timedelta(days=1))
t1 = ts.utc(startTime + timedelta(weeks=1))

def compute_sunrise_sunset(location, cityName, t0, t1):
    t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(ephem, location))
    for t, is_sunrise in zip(t, y):
        if is_sunrise:
            print("sunrise @"+cityName+": " + t.astimezone(utc).strftime('%Y-%m-%d %H:%M:%S %Z'))
        else:
            print("sunset @"+cityName+" : "+ t.astimezone(utc).strftime('%Y-%m-%d %H:%M:%S %Z'))


location = api.Topos(latitude_degrees=float(CITY['lat']), longitude_degrees=float(CITY['lon']), elevation_m=CITY['elevation'])

compute_sunrise_sunset(location, CITY['name'], t0, t1)
