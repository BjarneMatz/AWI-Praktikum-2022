from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="sensor")
point = locator.geocode("Neumayer Station III")
print(point.latitude)
