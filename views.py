import tornado.web
from cassandra.cluster import Cluster
from models import *
from serializer import *


class countriesHandler(tornado.web.RequestHandler):

	def get(self):
		q = Country.objects().all()

		data = [CountrySerializer(data=i).get_dict() for i in q]
		self.write({"country":data})


class countriesByIsoHandler(tornado.web.RequestHandler):

	def get(self, pk):
		try:
			q = Country.objects().all()
			data = [CountrySerializer(data=i).get_dict() for i in q if i.iso==pk]
		except:
			data =[]
		self.write({pk:data})

class citiesHandler(tornado.web.RequestHandler):

	def get(self, pk):

		try:
			q = City.objects().all()
			data = [CitySerializer(data=i).get_dict() for i in q if i.country_id==pk]
		except:
			data = []
		self.write({pk:data})
