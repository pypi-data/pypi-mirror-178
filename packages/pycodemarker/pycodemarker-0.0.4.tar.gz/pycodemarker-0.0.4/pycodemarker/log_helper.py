import logging

import ecs_logging

class Logger():

	def __init__(self):
		self.logger = logging.getLogger('codemarker-logstash-logger')
		self.logger.setLevel(logging.INFO)
		handler = logging.FileHandler('droidlogs.json')
		handler.setFormatter(ecs_logging.StdlibFormatter())
		self.logger.addHandler(handler)

	def info(self, msg, extras):
		self.logger.info(msg, extra=extras)

