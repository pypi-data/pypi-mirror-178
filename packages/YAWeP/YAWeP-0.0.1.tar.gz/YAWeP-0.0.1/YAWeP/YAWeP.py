# YAWeP -->> Yet another weather package
# Author: Leihaorambam Abhijit Singh

import requests

class Weather():
	"""
	Create a weather object and needs apikey.
	Weather object argument should be city or lat and lon
	For example:
	>>> weather_obj = Weather(apikey="YOUR_API_KEY",city="YOUR_CITY",lat=12.1,lon=12.2)
	
	>>> weather_obj.next_12h() # gives you the whole dataset

	>>> weather_obj.next_12h_simplified() # gives you a simplified dataset

	"""
	def __init__(self, apikey, city=None, lat=None, lon=None):
		if city:
			r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric")
			self.data = r.json()
		elif lat and lon:
			r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=metric")
			self.data = r.json()
		else:
			raise TypeError("No argument provided for city or lat and long")

		if self.data['cod'] != "200":
			raise ValueError(self.data["message"])

	def next_12h(self):
		"""
		Return 3 hours worth of data for next 12 hours as a dict
		"""
		return self.data['list'][:4]

	def next_12h_simplified(self):
		"""
		Return simplified 3 hours worth of data for next 12 hours as a tuple
		It returns date,temp,and sky condition.
		"""
		s_data = []
		for data in self.data['list'][::4]:
			s_data.append((data['dt_txt'], data['main']['temp'],data['weather'][0]['description']))
		return s_data