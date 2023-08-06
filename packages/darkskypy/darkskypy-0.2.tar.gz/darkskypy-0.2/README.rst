DarkSkyPy - Python 3
============
A Different Python3 wrapper for the [DarkSky.net](https://www.darksky.net) API.

Rewriting the API to reduce clutter and make obtaining data much more flexible. Based heavily off David Ervideira's forecastiopy.

This API is a work in progress, still very rough not guaranteed to work.
Please use [forecastiopy](https://github.com/dvdme/forecastiopy) (python2.7) or  [forecastiopy3](https://github.com/bitpixdigital/forecastiopy3) (python3) if you actually need an API


Powered by [Dark Sky](https://darksky.net/poweredby/)

####Quick Start:
Install the package:
```
python setup.py install
```

Get the coordinates of your location, let's say Lisbon:
```python
>>> Lisbon = [38.7252993, -9.1500364]
```

Get the current temperature and precipitation probability:
```python
>>> from darkskypy import DarkSky
>>> ds = DarkSky(Lisbon, key=YOUR_APY_KEY)
>>> current_temp = ds.forecast.currently.temperature
>>> print('Temperature:', current_temp)
Temperature: 11.07
>>> print('Precipitation Probability:', ds.forecast.currently.precipProbability)
Precipitation Probability: 0.29
```
####Function:

* Read Data Points and Data blocks from the [DarkSky.net](https://darksky.net/dev/) API.

Sets up a a hierarchical dictionary object that allows easy access to the currently, minutely, hourly, daily, etc. reports with their nested data. Data can be accessed directly by attributes as a [AttrDict](https://pypi.python.org/pypi/attrdict/2.0.0) object. See Package for more information on how AttrDict works.

Please refer to the API docs [https://darksky.net/dev/docs/forecast](https://darksky.net/dev/docs/forecast) for better understanding of how the Forecast Request is structured and what parameters can be set.

####To Do:
* Actually test this API
* Fix, setup.py
* Improve the docstrings


####Dependencies:
* [requests](https://pypi.python.org/pypi/requests/)
* [AttrDict](https://pypi.python.org/pypi/attrdict/2.0.0)

API Overview
--------------

**Setting API Key**
The required API key can be passed as a kwarg or stored on in your system's environmental variables.
```bash
$ export DARKSKY_API_KEY=<API Key>

```

**Initialize the DarkSky class**
The location should be provided as a list of [latitude,longitude]. Coordinates can be easily obtained from a Geocoding API such as [geocoder](https://github.com/DenisCarriere/geocoder). Optional Parameters are passed as kwargs following the API doc.
```python
import darkskypy
import geocoder

g = geocoder.google('Washington, DC')

ds = darkskypy.DarkSky(g.latlng, exclude='minutely,hourly', units='si')
# g.latlng >>> [38.9071923, -77.0368707]
# excludes minutely and hourly data blocks and reports in si units.
```

**Get Currently weather data for the requested location**
```python
if ds.forecast.currently is True:
	for element in ds.forecast.currently:
		print(element + ' : ' + str(ds.forecast.currently[element]))
	# Or access attributes directly
	print(ds.forecast.currently.temperature)
	print(ds.forecast.currently.humidity)
else:
	print('No Currently data')
```
**Get Daily weather data for the requested location**
The data blocks for Minutely, hourly, and daily data are dictionary sequences that represent each time unit. (i.e. hourly: hours in day, Daily: days in week)

```python
if ds.forecast.daily is True:
	print('Summary:', ds.forecast.daily.summary)
	print('Icon:', ds.forecast.daily.icon)
  # these would relate to the whole Daily block i.e. "the week"

	for day in ds.forecast.daily.data:
    print('Day summary: '+ day.summary)
    # prints the 'summary' for each day

  print(ds.forecast.daily.data[0].summary)
  #accessed directly
else:
	print('No Daily data')
```

**Alerts and Flags weather data** should work just like Flags and the other ones, but at the time I am writing this, I could not find a location with alerts to test on.

**A note on time**
The API returns time in unix time. Although this is a good computer format, it is not particulary _human-readable_. The datatime module can be used to get a more useful format.
```python
import datetime

time = datetime.datetime.fromtimestamp(int(currently.time).strftime('%Y-%m-%d %H:%M:%S')
print('unix time:', currently.time)
print('time:', time)

```

Output should be like:
```
unix time: 1448234556
time: 2015-11-22 23:22:36
```

Issues
------
Please report any issues at [Github](https://github.com/mattbox/DarkSkyPy)
