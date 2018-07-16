from models import *
country_key_list = ["id", "iso", "iso3", "name", "name_localized", "capital", "currency_code", "currency_name",
			"languages", "phone", "tld", "postal_code_format", "postal_code_regex", "neighbours", "geo_name_id",
			"created_at", "updated_at"]

city_key_list = ["id", "gh_numeric", "city_status", "name", "name_localized", "country_id", "region_id", 
			"district_id", "is_clinics_exists", "is_diagnostics_exists", "is_doctors_exists", "is_laboratories_exists",
			"latitude", "longitude", "location_accuracy", "created_at", "updated_at"]

with  open("geo_country.csv") as f:
	for s in f:
		s_line = s.split(",")
		data = {}
		for i, s in zip(country_key_list, s_line):
			data[i] = s
		c = Country(**data)
		c.save()

with  open("geo_city.csv") as f:
	for s in f:
		s_line = s.split(",")
		for i, s in zip(city_key_list, s_line):
			data[i] = s
		c = City(**data)
		c.save()
