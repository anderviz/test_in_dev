import json

class CountrySerializer():

	def __init__(self, data):
		self.init_data = data

	def get_dict(self):
		key_list = ["id", "iso", "iso3", "name", "name_localized", "capital", "currency_code", "currency_name",
			"languages", "phone", "tld", "postal_code_format", "postal_code_regex", "neighbours", "geo_name_id",
			"created_at", "updated_at"]

		return {i:getattr(self.init_data, i) for i in key_list}




class CitySerializer():

	def __init__(self, data):
		self.init_data = data

	def get_dict(self):
		key_list = ["id", "gh_numeric", "city_status", "name", "name_localized", "country_id", "region_id", 
			"district_id", "is_clinics_exists", "is_diagnostics_exists", "is_doctors_exists", "is_laboratories_exists",
			"latitude", "longitude", "location_accuracy", "created_at", "updated_at"]

		return {i:getattr(self.init_data, i) for i in key_list}

