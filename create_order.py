from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trade_declarative import *
import datetime
import random

engine = create_engine('sqlite:///sqlalchemy_example1.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


if __name__ == '__main__':
	time = datetime.datetime.now()
	pair0 = Pair(min_price=0.1, max_price=1000, name="BTC/LTC")
	pair = Pair(min_price=0.1, max_price=1000, name="QTUM/LTC")
	pair2 = Pair(min_price=0.1, max_price=1000, name="QTUM/BTC")
	pair3 = Pair(min_price=0.1, max_price=1000, name="ETH/BTC")
	pair4 = Pair(min_price=0.1, max_price=1000,name="ETH/LTC")
	pair5 = Pair(min_price=0.1, max_price=1000, name="ETH/QTUM")
	session.add(pair0)
	session.add(pair)
	session.add(pair2)
	session.add(pair3)
	session.add(pair4)
	session.add(pair5)
	session.commit()
	time = datetime.datetime.now()
	time_to_add = time - datetime.timedelta(minutes=1600)

	t1 = Trade(quantity=1, amount=4, price=34, time=time, order_from=1, order_to=3, pair=1)
	t2 = Trade(quantity=1, amount=4, price=514, time=time, order_from=1, order_to=3, pair=2)
	t3 = Trade(quantity=1, amount=4, price=218, time=time, order_from=1, order_to=3, pair=3)
	t4 = Trade(quantity=1, amount=4, price=235.796, time=time, order_from=1, order_to=3, pair=4)
	t5 = Trade(quantity=1, amount=4, price=345.234554, time=time, order_from=1, order_to=3, pair=5)
	t6 = Trade(quantity=1, amount=4, price=22.324, time=time, order_from=1, order_to=3, pair=6)

	
	session.add(t1)
	session.commit()
	session.add(t2)
	session.commit()
	session.add(t3)
	session.commit()
	session.add(t4)
	session.commit()
	session.add(t5)
	session.commit()
	session.add(t6)
	session.commit()

