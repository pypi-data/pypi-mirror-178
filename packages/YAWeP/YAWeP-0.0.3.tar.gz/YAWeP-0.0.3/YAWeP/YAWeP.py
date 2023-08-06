# YAWeP -->> Yet another weather package
# Author: Leihaorambam Abhijit Singh

import requests

class Weather():
	"""
	YAWeP -->> Yet another weather package
	Author: Leihaorambam Abhijit Singh
	Create a weather object and needs apikey.
	Weather object argument should be city or lat and lon
	Gives data in Metric
	Data is from OpenWeatherMap
	For example:
	>>> weather_obj = Weather(apikey="YOUR_API_KEY",city="YOUR_CITY") # with only city name
	>>> weather_obj = Weather(apiKey="YOUR_API_KEY",None,lat="Lattitude",lon="Longitude")
	
	>>> weather_obj.next_12h() # gives you the whole data

	>>> weather_obj.next_12h_simplified() # gives you a simplified data

	>>> weather_obj.current_h() # gives current hour data

	>>> weather_obj.current_h_simplified() # gives current hour temp,humidity,pressure,description, and icon

	"""
	def __init__(self, apikey, city=None, lat=None, lon=None):

		#attributes
		self.city = city

		if city:
			# Get data for next 5days 
			next_12h = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric")
			self.data_next_12h = next_12h.json()

			# Get data for current hour
			current_h = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&units=metric")
			self.data_current_h = current_h.json()

		elif lat and lon:
			# Get data for next 5days
			next_12h = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=metric")
			self.data_next_12h = next_12h.json()

			# Get data for current hour
			current_h = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=metric")
			self.data_current_h = current_h.json()

			# Get data for solar radiation
			solar_rad = requests.get(f"http://api.openweathermap.org/data/2.5/solar_radiation?lat={lat}&lon={lon}&appid={apikey}")
			self.data_solar_rad = solar_rad.json()
		else:
			raise TypeError("No argument provided for city or lat and long")

		if self.data_next_12h['cod'] != "200":
			raise ValueError(self.data_next_12h["message"])
		if self.data_current_h['cod'] != 200:
			raise ValueError(self.data_current_h["message"])

	def current_h(self):
		"""
		Return Current Hour data as a dict
		"""
		return self.data_current_h

	def current_h_simplified(self):
		"""
		Return Current Hour data in simplified as tuple
		Temp, pressure , humidity , description , icon code
		"""
		c_data = []
		c_data.append((self.data_current_h['main']['temp'],self.data_current_h['main']['pressure'],self.data_current_h['main']['humidity'],self.data_current_h['weather'][0]['description'],self.data_current_h['weather'][0]['icon']))
		return c_data

	def next_12h(self):
		"""
		Return 3 hours worth of data for next 12 hours as a dict
		"""
		return self.data_next_12h['list'][:4]

	def next_12h_simplified(self):
		"""
		Return simplified 3 hours worth of data for next 12 hours as a tuple
		It returns date, temp, sky condition, and icon code
		"""
		s_data = []
		for data in self.data_next_12h['list'][::4]:
			s_data.append((data['dt_txt'], data['main']['temp'],data['weather'][0]['description'],data['weather'][0]['icon']))
		return s_data

	def current_solar_radiation(self):
		"""
		Return Solar radiation data based on the lat and lon given
		Needed you need to have api ascess for this
		"""
		if self.city != None:
			raise ValueError("Solar radiation is currenlty not supported for city only with lat and lon")
		else:
			return self.data_solar_rad