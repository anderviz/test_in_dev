import tornado.web
from cassandra.cluster import Cluster
from models import *
from serializer import *


class countriesHandler(tornado.web.RequestHandler):

<<<<<<< HEAD
=======

def to_big_int(num):
	return int(num*10**8)



def to_float(num):
	return float(num/10**8)





def try_close(order):
	if order.type == 'sell':
		type = 'buy'
		order_by_value = Order.price.desc()
		order_func = lambda order, old_order: order.price <= old_order.price
		coinid_for_new = order.get_pair().name.split('/')[1]
		coinid_for_old = order.get_pair().name.split('/')[0]
	else:
		type = 'sell'
		order_by_value = Order.price
		order_func = lambda order, old_order: order.price >= old_order.price
		coinid_for_new = order.get_pair().name.split('/')[0]
		coinid_for_old = order.get_pair().name.split('/')[1]	
	active_order = session.query(Order).filter_by(status=False, type=type).order_by(order_by_value, 'time')


	for old_order in active_order:
		if order_func(order, old_order) and to_big_int(order.quantity) - to_big_int(old_order.quantity) >= 0:
			
			trade_quantity = old_order.quantity
			trade_price = old_order.price
			trade_amount = old_order.price * old_order.quantity * 0.98
			if to_big_int(trade_amount):
				result_order = refill_client.request(method_name="refill_inc",  
					uid=str(order.user_id), value=to_big_int(trade_amount), coinid=coinid_for_new, table='Trade')
			if to_big_int(trade_quantity):
				result_old_order = refill_client.request(method_name="refill_inc",  uid=str(old_order.user_id),
					value=to_big_int(trade_quantity), coinid=coinid_for_old, table='Trade')

			if correct_refil in result_order and correct_refil in result_old_order:	
				trade = Trade(order_from=old_order.id, order_to=order.id ,quantity=trade_quantity, 
					time=datetime.datetime.now().isoformat(), amount=trade_amount, price=trade_price, pair=order.pair)
				if trade.quantity and trade.amount:
					session.add(trade)
				session.commit()
				order.quantity = to_float(to_big_int(order.quantity) - to_big_int(old_order.quantity))
				old_order.status = True

				#history_client.request(method_name="insert", table="TradeHistory",
               	#		fields={'id': trade.id, 'quantity':trade.quantity, 'user_to':trade.order_to,
               	#			'user_from':trade.order_from, 'amount':trade.amount, 'price':trade.price})
			else:
				break
			
		elif order_func(order, old_order) and to_big_int(order.quantity) - to_big_int(old_order.quantity) < 0:
			trade_quantity = order.quantity
			trade_price = old_order.price
			trade_amount = old_order.price * order.quantity * 0.98
			
			if to_big_int(trade_amount):
				result_order = refill_client.request(method_name="refill_inc",  uid=str(order.user_id),
					value=to_big_int(trade_amount), coinid=coinid_for_new, table='Trade')
			if to_big_int(trade_quantity):
				result_old_order = refill_client.request(method_name="refill_inc",  uid=str(old_order.user_id),
					value=to_big_int(trade_quantity), coinid=coinid_for_old, table='Trade')
			
			if correct_refil in result_order and correct_refil in result_old_order:			
				trade = Trade(order_from=old_order.id, order_to=order.id, quantity=trade_quantity,
					time=datetime.datetime.now().isoformat(), amount=trade_amount, price=trade_price, pair=order.pair)
				if trade.quantity and trade.amount:
					session.add(trade)
				session.commit()
				old_order.quantity = to_float(to_big_int(old_order.quantity) - to_big_int(order.quantity))
				order.quantity = 0
				#history_client.request(method_name="insert", table="TradeHistory", 
				#		fields={'id': trade.id, 'quantity':trade.quantity,  'user_to':trade.order_to,
				#			'user_from':trade.order_from, 'amount':trade.amount, 'price':trade.price})
				session.commit()
				
			else:
				break
			
		else:
			break

	if not order.quantity:
		order.status = True
		
	session.commit()



class BaseHandler(tornado.web.RequestHandler):
	def set_default_headers(self, *args, **kwargs):
		self.set_header("Access-Control-Allow-Origin", "http://localhost:8080")
		self.set_header("Access-Control-Allow-Headers", "accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with, Cache-Control")
		self.set_header("Access-Control-Allow-Methods", "DELETE, GET, OPTIONS, PATCH, POST, PUT")
		self.set_header('Access-Control-Request-Headers', "DELETE, GET, OPTIONS, PATCH, POST, PUT")
		self.set_header("Allow", "DELETE, GET, OPTIONS, PATCH, POST, PUT")
		self.set_header('Access-Control-Allow-Credentials', True)



class PairHandler(BaseHandler):
	@tornado.web.asynchronous
	def get(self):
		pair_list = []
		for i in session.query(Pair):
			pair_list.append({'id':i.id, 'name':i.name, 'min_price':i.min_price, 'max_price':i.max_price})
		self.write(json.dumps(pair_list))
		self.finish()



class CreateOrderHandler(BaseHandler):
	def post(self):
		try:
			pair = self.get_argument('pair')
			quantity = self.get_argument('quantity')
			price = float(self.get_argument('price'))
			type = self.get_argument('type')
			user_id = self.get_argument('user_id')
		except:
			self.write('Не коректные аргументы')
		try:
			pair = session.query(Pair).filter_by(name=pair).one()
		except:
			self.write('error pair')
		
		user_id = self.get_argument('user_id')

		new_order = Order(pair=pair.id, quantity=float(quantity), user_id=user_id, 
		price=float(price), status=False, type=type, time=datetime.datetime.now().isoformat())
		if new_order.valid():
			new_order.set_amount()
			if new_order.check_balance():
				try:
					session.add(new_order)
					session.commit()
					
				except:
					self.write('Data base Eror')
				if new_order.reset_user_balance():
					self.write(json.dumps({'order_id':new_order.id, 'result':True}))
					history_client.request(method_name="insert", table="Orders",
               				fields={'id': new_order.id, 'pair': new_order.pair, 
               					'quantity':new_order.quantity, 'user_id':new_order.user_id, 'amount':new_order.amount,
               					'price':new_order.price})
					session.commit()
				else:
					session.delete(new_order)
					
					self.write({'error':True, 'code':101})
					return
			else:
				self.write({'error':True, 'code':102})
				return
		else:
			self.write({'error':True, 'code':102})
			return
		
		try_close(new_order)



class OrderBookHandler(BaseHandler):
>>>>>>> 66275c8b09adf1c9f9cba3d27fe86d81c1d26f08
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

<<<<<<< HEAD
	def get(self, pk):
		print (pk)
		try:
			q = City.objects().all()
			data = [CitySerializer(data=i).get_dict() for i in q if i.country_id==pk]
		except:
			data = []
		self.write({pk:data})
=======

class PairHistoryHandler(BaseHandler):
	def get(self):
		try:
			pair = self.get_argument('pair')
			
		except:
			self.write({'error':True, 'code':102})
			return
		try:
			pair = session.query(Pair).filter_by(name=pair).one()

		except:
			self.write({'error':True, 'code':102})
			return
		try:
			minute = int(self,get_argument('minute'))
		except:
			minute = 1

		data = []
		for i in session.query(TradeHistory).filter_by(pair=pair.id).order_by(TradeHistory.id.desc()).limit(minute):
			data.append([i.time_start, i.open_price, i.high_price, i.low_price, i.close_price])
		self.write({'history':data})


class TradesHistoryHandler(BaseHandler):
	def get(self):
		data = []
		for i in session.query(Trade).filter_by().order_by(Trade.id.desc()).limit(200):
			if not i.price:
				continue
			try:
				data.append({'time':i.time, 'pair':i.get_pair().name, 'type':i.get_order_from().type, 'price':i.price, 'quantity':i.quantity, 'amount':i.amount})
			except:
				continue
		self.write({'trades':data})

class PairStatsHandler(BaseHandler):
	def get(self):
		data = []
		for i in session.query(Pair):
			last_trade = session.query(Trade).filter_by(pair=i.id).order_by(Trade.time.desc()).first()
			top_sell_order = session.query(Order).filter_by(status=False, type='sell').order_by(Order.price, 'time').first()
			top_buy_order = session.query(Order).filter_by(status=False, type='buy').order_by(Order.price.desc(), 'time').first()
			data.append({'name':i.name, 'sell':top_sell_order, 'buy':top_buy_order})
		self.write({'stats':data})
>>>>>>> 66275c8b09adf1c9f9cba3d27fe86d81c1d26f08
