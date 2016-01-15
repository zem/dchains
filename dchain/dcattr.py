#!/usr/bin/python3
import hashlib
import gnupg
import sys, os
import magic
import yaml
import re
from datetime import datetime
import dchain.dcconf
import dchain.dcdoc
from dchain.dcconf import * 
from dchain.dcconf import *
__all__=['dcattr']



class dcattr():
	""" 
	__init__
	--------
	init always needs a document object to attach to, it can't stay alone
	however it can either be created by setting name value coment and ts 
	or it can be loaded by providing an attribute id 
	"""
	def __init__(self, doc, 
		name='', value='', comment='', ts=datetime.utcnow(),
		dcattrid='',
		dcattrfilename='',
	):
		# link gpg over to this object
		self.gpg=doc.gpg
		self.dcattrid=''
		if doc=='':
			raise Exception("dcattr needs a dchains.doc object to do work")
		self.doc=doc
		if dcattrfilename!='':
			dcattrid=re.sub('\.dcattr$', '', dcattrfilename)
		if dcattrid=='':
			self.a={
				doc.dcdocid: {
					'name': name,
					'value': value,
					'comment': comment,
					'ts': str(ts),
				}
			}
			self.ts=ts
		else:
			self._load_dcattrid(dcattrid)
	def _load_dcattrid(self, dcattrid):
		self.dcattrid=dcattrid
		f=open(self.doc.workdir()+"/"+dcattrid+".dcattr", "rb")
		content=f.read()
		f.close()
		verified=self.gpg.verify(content)
		if not verified: raise Exception("Signature could not be verified!")
		self.verified=verified	# can be used to query the who and where 
		sha=hashlib.sha256()
		sha.update(content)
		if sha.hexdigest() != dcattrid:
			raise Exception("checksum mismatch during load of dcattr from storage")	
		# TODO Better verification here 
		data=self.gpg.decrypt(content)
		self.a=yaml.load(str(data))
		if not self.doc.dcdocid in self.a:
			raise Exception("Documentid must be stored in dataset!")	
	def save(self):
		dcattrsig=self.gpg.sign(yaml.dump(self.a, default_flow_style=False),
			keyid=self.doc.keyid,
		)
		sha=hashlib.sha256()
		sha.update(dcattrsig.data)
		dcattrid=sha.hexdigest()
		if self.dcattrid != '':
			raise Exception("the object already has a dcattrid configured")	
		self.dcattrid=dcattrid
		if os.path.exists(self.doc.workdir()+"/"+dcattrid+".dcattr"):
			raise Exception("the file that should contain this attributes data already exists!")	
		f=open(self.doc.workdir()+"/"+dcattrid+".dcattr", "wb")
		f.write(dcattrsig.data)
		f.close()
	def lookup(self, key):
		return self.a[self.doc.dcdocid][key]
	def value(self):
		return self.lookup('value')
	def name(self):
		return self.lookup('name')
	def comment(self):
		return self.lookup('comment')
	def ts(self):
		return date.datetime(self.lookup('ts'))

