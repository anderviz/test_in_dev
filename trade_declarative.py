import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests

import json
from jsonrpcclient.http_client import HTTPClient

from config import *


refill_client = HTTPClient(refill_host)
balance_client = HTTPClient(balance_host)
history_client =  HTTPClient(history_host)


Base = declarative_base()
engine = create_engine('sqlite:///sqlalchemy_example1.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Pair(Base):
	__tablename__ = 'pair'
	id = Column(Integer, primary_key=True)
	min_price = Column(Float, nullable=False)
	max_price = Column(Float, nullable=False)
	name = Column(String(250), nullable=False)


class TradeHistory(Base):
	__tablename__ = 'history_trade'
	id = Column(Integer, primary_key=True)
	time_start = Column(Integer, nullable=False)
	time_end = Column(Integer)
	open_price = Column(Float)
	close_price = Column(Float)
	high_price = Column(Float)
	low_price = Column(Float)
	pair = Column(Integer, ForeignKey('pair.id'), nullable=False)
	total = Column(Float, nullable=True)

class Order(Base):
	__tablename__ = 'order'
	id = Column(Integer, primary_key=True)
	pair = Column(Integer, ForeignKey('pair.id'), nullable=False)
	quantity = Column(Float, nullable=False)
	status = Column(Boolean, nullable=False)
	user_id = Column(Integer, nullable=False)
	amount = Column(Float, nullable=True)
	price = Column(Float, nullable=True)
	type = Column(String(250), nullable=False)
	time = Column(Integer, nullable=False)

	def valid(self):
		if self.type != 'sell' and self.type != 'buy':
			return False
		if self.price >= self.get_pair().min_price and self.price <= self.get_pair().max_price:
			return True
		else:
			return False

	def get_pair(self):
		return session.query(Pair).filter_by(id=self.pair).one()

	def set_amount(self):
		self.amount = self.quantity * self.price

	def check_balance(self):
		coinid = None

		if len(self.get_pair().name.split('/')) != 2:
			return False

		if self.type == "sell":
			coinid = self.get_pair().name.split('/')[0]
		else:
			coinid = self.get_pair().name.split('/')[1]
		
		try:
			balance = balance_client.request(method_name='getbalance', uid=self.user_id, coinid=coinid)		
			float(balance)
		except:
			return False
		if self.type == 'sell':
			return self.quantity <= balance
		else:
			return self.amount <=  balance
		
	
	def reset_user_balance(self):
		coinid = None
		if len(self.get_pair().name.split('/')) != 2:
			return False
		
		if self.type == 'sell':
			coinid = self.get_pair().name.split('/')[0]
			value = int(self.quantity*10**8)

		else:
			coinid = self.get_pair().name.split('/')[1]
			value = int(self.amount*10**8)
		
		result = refill_client.request(method_name="refill_dec",  uid=str(self.user_id), value=value, coinid=coinid, table='Trade')
		if "successfully" in result:
			return True
		else:
			return False

	def set_quantity(self, quantity):
		setattr(self, 'quantity', quantity)
		session.commit()


class Trade(Base):
	__tablename__ = 'trade'
	id = Column(Integer, primary_key=True)
	quantity = Column(Float, nullable=False)
	amount = Column(Float, nullable=False)
	price = Column(Float, nullable=False)
	time = Column(Integer, nullable=False)
	order_from = Column(Integer, ForeignKey('order.id'), nullable=False)
	order_to = Column(Integer, ForeignKey('order.id'), nullable=True)
	pair = Column(Integer, ForeignKey('pair.id'), nullable=True)

	def get_order_from(self):
		return session.query(Order).filter_by(id=self.order_from).one()
	

	def get_order_to(self):
		return session.query(Order).filter_by(id=self.order_to).one()

	def get_pair(self):
		pair = session.query(Pair).filter_by(id=self.pair).one()
		return pair


engine = create_engine('sqlite:///sqlalchemy_example1.db')
Base.metadata.create_all(engine)

history_client.request(method_name="create_table", table='Orders',
               fields={'id': ['int(64, unsigned)', 'yes'], 'pair': ['int(32, unsigned)', 'no'], 
               'quantity':['float(32)', 'no'], 'user_id':['int(32, unsigned)', 'no'], 'amount':['float(32)', 'no'], 'price':['float(32)', 'no'], 'time':['int(32, unsigned)', 'no'] })

history_client.request(method_name="create_table", table='TradeHistory',fields={'id': ['int(64, unsigned)','yes'], 'user_from':['int(32, unsigned)', 'no'], 'user_to':['int(32, unsigned)', 'no'] , 'quantity':['float(32)', 'no'], 'amount':['float(32)', 'no'], 'price':['float(32)', 'no'], 'time':['int(32, unsigned)', 'no']})
#history_client.request(method_name='select', table='Trade', fields="*", query="") 