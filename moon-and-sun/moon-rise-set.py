from datetime import timedelta
import datetime
from pytz import utc
from skyfield import api, almanac
import numpy as np

MEAN_MOON_DISTANCE = 384402.  # km (semi major axis)
MEAN_MOON_DIAMETER = 3476.  # km
MEAN_APPARENT_MOON_DIAMETER = (MEAN_MOON_DIAMETER / MEAN_MOON_DISTANCE) * 180. / np.pi

REFRACTION = -0.34/60.
HORIZON = -MEAN_APPARENT_MOON_DIAMETER + REFRACTION

CITY = {'lat': '-19.746975', 'lon': '149.207542', 'name':'Hardy Reef'}

startTime = utc.localize(datetime.datetime.strptime('2023-10-01 12:00', '%Y-%m-%d %H:%M'))

SKYFIELD_DATA_DIR = './'
load = api.Loader(SKYFIELD_DATA_DIR)
eph = load('de421.bsp')
ts = load.timescale()
moon = eph['moon']
myloc = api.Topos(latitude_degrees=float(CITY['lat']), longitude_degrees=float(CITY['lon']))
f = almanac.risings_and_settings(ephemeris=eph, target=moon, topos=myloc, horizon_degrees=HORIZON)

t0 = ts.utc(startTime - timedelta(days=1))
t1 = ts.utc(startTime + timedelta(weeks=1))

def moon_skyfield(t0, t1):
    for t, updown in zip(*almanac.find_discrete(t0, t1, f)):        
        print(('Moon rise' if updown else 'Moon set ') + " @"+CITY['name']+": " + t.astimezone(utc).strftime('%Y-%m-%d %H:%M:%S %Z'))

moon_skyfield(t0, t1)