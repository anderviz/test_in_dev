import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model

class Country(Model):
	id = columns.Text(primary_key=True) 
	iso = columns.Text(required=False, custom_index=True)
	iso3 = columns.Text(required=False)
	name = columns.Text(required=False)
	name_localized = columns.Text(required=False)
	capital = columns.Text(required=False)
	currency_code = columns.Text(required=False)
	currency_name = columns.Text(required=False)
	languages = columns.Text(required=False)
	phone = columns.Text(required=False)
	tld = columns.Text(required=False)
	postal_code_format = columns.Text(required=False)
	postal_code_regex = columns.Text(required=False)
	neighbours = columns.Text(required=False)
	geo_name_id = columns.Text(required=False)
	created_at = columns.Text(required=False)
	updated_at= columns.Text(required=False)

class City(Model):
	id = columns.Text(primary_key=True) 
	gh_numeric = columns.Text(required=False)
	city_status = columns.Text(required=False) 
	name = columns.Text(required=False)
	name_localized = columns.Text(required=False)
	country_id = columns.Text(required=False, custom_index=True)
	region_id = columns.Text(required=False)
	district_id = columns.Text(required=False)
	is_clinics_exists = columns.Text(required=False)
	is_diagnostics_exists = columns.Text(required=False)
	is_doctors_exists = columns.Text(required=False)
	is_laboratories_exists = columns.Text(required=False)
	latitude = columns.Text(required=False)
	longitude = columns.Text(required=False)
	location_accuracy = columns.Text(required=False)
	created_at = columns.Text(required=False)
	updated_at = columns.Text(required=False)

connection.setup(['127.0.0.1'], "testtask", protocol_version=3)

sync_table(Country)
connection.setup(['127.0.0.1'], "testtask", protocol_version=3)
sync_table(City)

print (City.objects.count())