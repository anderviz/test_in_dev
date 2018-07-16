
import sys
import os
import tornado.ioloop

# Module with entire endpoints
from endpoints import router
import datetime


if __name__ == '__main__':
	router.listen(8000)
	tornado.ioloop.IOLoop.current().start()