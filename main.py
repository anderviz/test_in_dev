
import sys
import os
import tornado.ioloop

# Module with entire endpoints
from endpoints import router
import datetime

<<<<<<< HEAD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


=======
		if minute:
			trades = session.query(Trade).filter_by(pair=pair_id.id).order_by(Trade.time.desc()).first()

						
			
			if not obj:
				p = 0
				if trades:
					p = trades.price

				new_history = TradeHistory(time_start=time.isoformat(), time_end=0, open_price=p,
					close_price=0, high_price=0, low_price=0, pair=pair_id.id)
				session.add(new_history)
				session.commit()



			else:
				if time - parser.parse(obj.time_start) <  datetime.timedelta(minutes=1):
					dif_time = time - parser.parse(obj.time_start)
					return
				

				part_order = session.query(Trade).filter_by(pair=pair_id.id)
				list_time = []
				c = 1

				#list_time = part_order
				for i in part_order:
					if i.time > obj.time_start:
						list_time.append(i)
				
				max_price = 0
				min_price = 10**8
				total_quantity = 0
				for i in list_time:
					if max_price < i.price:
						max_price = i.price
					if min_price > i.price:
						min_price = i.price
					total_quantity += i.quantity
				
				if min_price == 10**8:
					min_price = 0

				trade_last = session.query(Trade).filter_by(pair=pair_id.id).order_by(Trade.time.desc()).first()
				if not trade_last:
					print ('!!!!!!!!!!')
					continue
				obj.time_end = time
				obj.close_price = trade_last.price
				if not max_price:
					obj.high_price = obj.open_price
				else:
					obj.high_price = max_price

				if not min_price:
					obj.low_price = obj.open_price
				else:
					obj.low_price = min_price
				if obj.high_price < obj.open_price:
					obj.high_price - obj.open_price
				obj.total = total_quantity
				new_history = TradeHistory(time_start=time.isoformat(), time_end=0, open_price=trade_last.price,
					close_price=0, high_price=0, low_price=0, pair=pair_id.id, )
				session.add(new_history)
				session.commit()
				
>>>>>>> 66275c8b09adf1c9f9cba3d27fe86d81c1d26f08

if __name__ == '__main__':
	router.listen(8000)
	tornado.ioloop.IOLoop.current().start()