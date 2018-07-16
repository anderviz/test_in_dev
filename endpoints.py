import tornado.web
import views




router = tornado.web.Application([

	(r"^/country_by_iso/(?P<pk>.+)/$", views.countriesByIsoHandler),
	(r"^/country/(?P<pk>.+)/cities/$", views.citiesHandler),
	(r"^/countries/?$", views.countriesHandler),
], debug = True)


