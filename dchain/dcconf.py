import yaml
import os


class dcconf():
	def __init__(self, 
		user_dchainsrc=os.environ["HOME"]+"/.dchainsrc",
		system_dchainsrc="/etc/dchains.conf"
	):
		self.settings={
			'gpg_keyid': 'UNCONFIGURED',
			'gpg_bin': 'gpg2',
		}
		self.storage={
			'default': {
				'url': os.environ["HOME"]+"/.dchains/",
				# that index database is for future use, it will be filled by an indexer, and provides fast access
				'index': 'sqllite://'+os.environ["HOME"]+"/.dchains/index.db",
			}
		}
		self.loadrc(system_dchainsrc)
		self.loadrc(user_dchainsrc)
		self.update_storage();
	def loadrc(self, rcfile):
		if os.path.exists(rcfile):
			f=open(rcfile, "r")
			rc=yaml.load(f.read())
			f.close()
			self.settings.update(rc['settings'])
			self.storage.update(rc['storage'])
	def update_storage(self):
		for name in self.storage.keys():
			self.storage[name].update(self.settings)	
