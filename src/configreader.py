import ConfigParser

class Singleton:
	
	_instance = None
	
	class Instance:
		def __init__(self):
			pass
	
	def singelton(self):
		first = False
		
		if Singleton._instance is None:
			first = True
			Singleton._instance = Singleton.Instance()

		self._EventHandler_instance = Singleton._instance
		return first
	
	def __getattr__(self, attr):
		return getattr(self._instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self._instance, attr, value)	

CONFIGFILE = 'client.conf'
class ConfigReader( Singleton ):
	
	_config = None
	
 	def __init__(self):
		if self.singelton():
			ConfigReader._config = ConfigParser.ConfigParser()
			self._config.read(CONFIGFILE)
		
	def print_all(self):
		for section in self._config.sections():
			print section
			for option in self._config.options(section):
				print " ", option, "=", self._config.get(section, option)

	def get(self, section, option):
		return self._config.get(section, option)


if __name__ == "__main__":
	print ConfigReader().get("app", "version")
