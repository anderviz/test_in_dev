import tornado.web
import views




router = tornado.web.Application([
<<<<<<< HEAD
	(r"^/country_by_iso/(?P<pk>.+)/$", views.countriesByIsoHandler),
	(r"^/country/(?P<pk>.+)/cities/$", views.citiesHandler),
	(r"^/countries/?$", views.countriesHandler),
], debug = True)

=======
    (r"/api/pair_settings/", views.PairHandler),
    (r"/api/order_create/", views.CreateOrderHandler),
    (r"/api/order_book/", views.OrderBookHandler),
    (r"/api/user_trades/", views.UserTradesHandler),
    (r"/api/user_open_orders/", views.UserOpenOrdersHandler),
    (r"/api/order_cancel/", views.OrderCancelHandler),
    (r"/api/pair_history/", views.PairHistoryHandler),
    (r"/api/trades_history/", views.TradesHistoryHandler),
    (r"/api/pair_stats/", views.PairStatsHandler),
], debug=True
)
>>>>>>> 66275c8b09adf1c9f9cba3d27fe86d81c1d26f08
