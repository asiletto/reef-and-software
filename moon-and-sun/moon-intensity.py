from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from pytz import utc
from datetime import timedelta
import datetime
import traceback

ts = load.timescale()

eph = load('de421.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

startYear=2023
YEARS=1

for year in range(YEARS):
  for month in range(12):
    for day in range(31):
      for hour in range(24):
        try:
          stringTime = utc.localize(datetime.datetime.strptime(str(startYear+year)+"-"+str(month+1)+"-"+str(day+1)+" "+str(hour)+":00", '%Y-%m-%d %H:%M'))
    
          t = ts.utc(startYear+year, month+1, day+1, hour, 00)
          e = earth.at(t)
          s = e.observe(sun).apparent()
          m = e.observe(moon).apparent()
          _, slon, _ = s.frame_latlon(ecliptic_frame)
          _, mlon, _ = m.frame_latlon(ecliptic_frame)
          phase = (mlon.degrees - slon.degrees) % 360.0
          percent = 100.0 * m.fraction_illuminated(sun)

          print(stringTime.strftime('%Y-%m-%d %H')+" phase: "+'{0:.1f}'.format(phase)+" percent: "+'{0:.1f}'.format(percent))
          
          epoch = int( t.utc_datetime().replace(tzinfo=datetime.timezone.utc).timestamp())
          
        except ValueError:
          pass
          #print("not valid date: " + str(startYear+year)+"-"+str(month+1)+"-"+str(day+1)) #lazy way to handle months day and leap years
#          traceback.print_exc()