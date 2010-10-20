import logging
import logging.handlers

class Logger:
	
	logger = None
	callable = {'debug':'', 'info':'', 'warn':'', 'error':'', 'critical':''}

	def __init__(self, name, format, filename, filesize = 1024, count = 1):
		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG)

		handler = logging.handlers.RotatingFileHandler(
				  filename, maxBytes=filesize, backupCount=count)
		logger.addHandler(handler)

		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		formatter = logging.Formatter(format)
		ch.setFormatter(formatter)
		logger.addHandler(ch)


	def __setattr__(self, method, value):
		if (self.callable.has_key(method)):
			call = "self.logger.%{method}('%{msg}')" % {'method':method, 'msg':value}
			print call
			eval(call) 
			print "CALLING"
			#return self.contents[self.headers[name]]
		else:
			raise AttributeError,name

		 #return self.callback(*self.args, **self.kwargs)
	 
	#logger.debug("debug message")
	#logger.info("info message")
	#logger.warn("warn message")
	#logger.error("error message")
	#logger.critical("critical message")

log = Logger(None, '', 'test.log', 1024, 1)
log.warn = "warning message"
