# 
# Hints for your editor: 
# This file is indented with tabs, so you might have to set 
# tabstop to a value which suits your needs, this is how tabs 
# should be used
#

import hashlib
import gnupg
import sys, os
import magic
import yaml
import re
from datetime import datetime
from dchain.dcattr import * 
from dchain.dcconf import *
__all__=['dcdoc']

"""
class dcdoc()
===========

"""
class dcdoc():
	"""
	__init__
	--------
	the class init provides us with all neccessary 
	information to load a document from either the fs or 
	the repo
	
	parameters: 

	- path: the path where the file is located (defaults to working dir)
	- filename: the filename to be loaded
	- content: the documents content, if there is no name yet on filesystem
	- dcdocid: the document id (sha256 hexadecimal checksum over the content)
	- keyid: which keyid should be used to sign documents and attachments
	- storebase: The directory where the document chains storage is located
	- gpgbin: defaults to gpg2
	"""
	def __init__(self, filename='', dcdocid='', content='',
		storage="default",
		config=dcconf(),
	):
		# copy all that neccessary stuff to self
		self.filename=filename
		self.dcdocid=dcdocid
	
		self.dcattrs=[]
		self.revoked_dcattrs={}
		self.dcattr_by_name={}
		self.dcattr_by_id={}
		
		self.config=config
		self.storage=storage
		self.keyid=config.storage[storage]['gpg_keyid']
		self.storebase=config.storage[storage]['url']
		self.gpgbin=config.storage[storage]['gpg_bin']
		self.gpg=gnupg.GPG(gpgbinary=config.storage[storage]['gpg_bin'])
		self.sha=hashlib.sha256()
		# we implement three modes , 
		# only a document id 
		# only a filename 
		# content and a filename given
		# there is something odd if we have both or none 
		#  at initialization
		if dcdocid=="" and filename=="" and content=="": 
			raise Exception("please set either content or dcdocid or give a filename to load")
		
		if dcdocid!="" and filename!="": 
			raise Exception("filename and dcdocid was given")
		
		if dcdocid!="" and content!="": 
			raise Exception("content and dcdocid was given")
		
		if filename!="" and content!="": 
			raise Exception("content and filename was given")
	
		if dcdocid!='':
			self._load_dcdocid(dcdocid)
		elif filename!='':
			self._load_filename(filename)
		elif content!='':
			self._load_content(content)
	"""
	save
	-----
	stores the document and to the storage, or updates the stored document 
	in the storage
	"""
	def save(self):
		self.save_content()
		self.sign()
	def verify_signatures(self):
		self.verified={}
		for sig_file in os.listdir(self.workdir()):
			if re.match('.*\.signature$', sig_file):
				f=open(self.workdir()+"/"+sig_file, 'rb')
				verified=self.gpg.verify_file(f, self.contentfile())
				f.close()
				if verified:
					self.verified[verified.fingerprint]=verified
					# PRINT Error or log stuff that the verification failed.... 
					# if so 
	def sign(self):
		self._require_memory_content()
		if not hasattr(self, "verified"):
			self.verify_signatures()
		signature=self.gpg.sign(self.content, 
			detach=True, 
			binary=True, 
			keyid=self.keyid
		)
		if signature.fingerprint in self.verified:
			# this document was already signed with our key
			return
		sha=hashlib.sha256()
		sha.update(signature.data)
		sigfile=self.workdir()+"/"+sha.hexdigest()+".signature"
		if os.path.exists(sigfile):
			raise Exception("signature "+sigfile+" is already there")
		f=open(sigfile, "wb")
		f.write(signature.data)
		f.close()
	def save_content(self):
		# store the document and all its objects 
		# to the repository
		self._require_memory_content()
		if os.path.exists(self.contentfile()):
			# TODO Check here if the document on the disk really is the document in memory 
			return
		f=open(self.contentfile(), "wb")
		f.write(self.content)
		f.close()
	
	"""
	_load_filename
	---------------------
	this internal method loads a filename into the objects content 
	and continued with _load_content()
	"""
	def _load_filename(self, filename):
		if not os.path.exists(filename):
			raise Exception("File "+filename+" does not exists!")
		f=open(filename, "rb")
		self._load_content(f.read())
		f.close()
	
	"""
	_load_content
	---------------------
	this internal method gets the documents content as an argument, 
	it then calculates the sha256 checksum and the working path
	"""
	def _load_content(self, content):
		if content=='':
			raise Exception("content is empty, thats stupid!")
		self.content=content
		self.sha.update(content)
		if self.dcdocid=='':
			self.dcdocid=self.sha.hexdigest()
		elif self.dcdocid != self.sha.hexdigest():
			raise Exception("uuups, we loaded a document to the content but its checksum does not match our dcdocid")
		# load attributes, too if there are any
		self._load_dcattrs()
	def _load_dcdocid(self, dcdocid):
		# there is not yet anything to do here yet 
		# but to raise an exception if the document is not in the pool
		if not os.path.exists(self.contentfile()):
			raise Exception("this document "+self.contentfile()+" does not exists in dchains storage")
		self.verify_signatures()
		if len(self.verified.keys()) < 1:
			raise Exception("found no verifyable signature for this document")
		# load attributes to object
		self._load_dcattrs()
	def _load_dcattrs(self):
		# as soon as we have a dcdocid we also have workdir()
		if not os.path.exists(self.workdir()): return 
		for dcattr_file in os.listdir(self.workdir()):
			if re.match('.*\.dcattr$', dcattr_file):
				self.append_dcattr(dcattr(self, dcattrfilename=dcattr_file))
	def append_dcattr(self, dcattr):
		self.dcattr_by_id[dcattr.dcattrid]=dcattr
		if not dcattr.name() in self.dcattr_by_name: self.dcattr_by_name[dcattr.name()]=[]
		if not dcattr.dcattrid in self.revoked_dcattrs:
			self.dcattr_by_name[dcattr.name()].append(dcattr)
		if dcattr.name() == "revoke":
			self.revoked_dcattrs[dcattr.value()]=dcattr
			# we may need to revoke a stored value as well
			if dcattr.value() in self.dcattr_by_id:
				revoked_attr=self.dcattr_by_id[dcattr.value()]
				# delete revoked_attr from named list
				if not revoked_attr.name() in self.dcattr_by_name: self.dcattr_by_name[revoked_attr.name()]=[]
				index=0
				for a in self.dcattr_by_name[revoked_attr.name()]:
					if a==revoked_attr:
						del self.dcattr_by_name[revoked_attr.name()][index]
					else:
						index=index+1
	def _require_memory_content(self):
		if not hasattr(self, "content"):
			self._load_filename(self.contentfile())
			return
		if self.content=='':
			self._load_filename(self.contentfile())
	def workdir(self):
		if self.dcdocid == '':
			raise Exception("no dcdocid which is needed to create the docdir/workdir")
		if not hasattr(self, 'docdir'):
			self.docdir=self.dcdocid[0:8]+"/"+self.dcdocid[8:16]+"/"+self.dcdocid[16:24]+"/"+self.dcdocid
		workdir=self.storebase+self.docdir
		if not os.path.isdir(workdir):
			os.makedirs(workdir)
		return(workdir)
	def contentfile(self):
		return(self.workdir()+"/"+self.dcdocid+".dat")
	def dcattr_values_dict(self, name):
		names={}
		for a in self.dcattr_by_name[name]:
			if not a.value() in names:
				names[a.value()]=a
		return(names)
	def dcattr_values(self, name):
		return(self.dcattr_values_dict(name).keys())
	def dcattr_add(self, name, value, comment=""):
		a=dcattr(self,
			name=name,
			value=value,
			comment=comment,
		);
		a.save()
		self.append_dcattr(a)
	def dcattr_revoke(self, dcattrid, comment=""):
		self.dcattr_add('revoke', dcattrid, comment)
	"""
	content_type()
	--------------
	returns the content_type of the document if any content type is there. 
	This method first checks for available attributes if there is no attribute 
	it uses magic to detect the content type and stores the result as a documents attribute
	"""
	def content_type(self, ctype=""):
		ct=self.dcattr_values('content-type')
		if len(ct)>0:
			# we have a content type set for the object
			if ctype != "" and ct[0] != ctype:
				# set new content type 
				oldattrid=self.dcattr_values_dict('content-type')[ct[0]].dcattrid
				self.dcattr_add("content-type", ctype, "set via content_type() param")
				self.dcattr_revoke(oldattrid)
				return ctype
			elif ctype != "" and ct[0] == ctype:
				return ctype
			else:
				return ct[0]
		else:
			# there is no mimetype set yet to this object
			if ctype=='': 
				if self.content == '':
					raise Exception("I have no content stored in the object")
				mime = magic.open(magic.MAGIC_MIME) 
				mime.load()
				ctype=mime.buffer(self.content)
			self.dcattr_add("content-type", ctype, "set via content_type() param")
			return ctype
	def newer_version(self):
		if self.newer_version:
			return self.newer_version
		for docid in self.dcattr_values('newer_version'):
			self.newer_version=dcdoc(dcdocid=docid, storage=self.storage, config=self.config)
			return self.newer_version
		return None
	def older_version(self):
		if self.older_version:
			return self.older_version
		for docid in self.dcattr_values('older_version'):
			self.older_version=dcdoc(dcdocid=docid, storage=self.storage, config=self.config)
			return self.older_version
		return None
	def sources(self):
		if not hasattr(self, 'source_docs'):
			self.source_docs={}
		sdocs=[]
		for docid in self.dcattr_values('source'):
			if not docid in self.source_docs:
				self.source_docs[docid]=dcdoc(dcdocid=docid, storage=self.storage, config=self.config)
			sdocs.append(self.source_docs[docid])
		return sdocs
	def attachments(self):
		if not hasattr(self, 'attached_docs'):
			self.attached_docs={}
		adocs=[]
		for docid in self.dcattr_values('attachment'):
			if not docid in self.attached_docs:
				self.attached_docs[docid]=dcdoc(dcdocid=docid, storage=self.storage, config=self.config)
			adocs.append(self.attached_docs[docid])
		return adocs
	def add_attachment(self, doc, comment='via add_attachment() from '):
		# attach a document to this object
		self.dcattr_add('attachment', doc.dcdocid, comment)
		doc.dcattr_add('source', self.dcdocid, comment)
	def add_source(self, doc, comment='via add_source from '):
		# attach a document to this object
		self.dcattr_add('source', doc.dcdocid, comment)
		doc.dcattr_add('attachment', self.dcdocid, comment)
	def names(self):
		return self.dcattr_values("name")
	def names_dict(self):
		return self.dcattr_values_dict("name")
	def tags(self):
		return self.dcattr_values("tag")
	def tags_dict(self):
		return self.dcattr_values_dict("tag")
	def add_name(self, name, comment="via add_name wizard"):
		return self.dcattr_add('name', name, comment)
	def add_tag(self, name, comment="via add_tag wizard"):
		return self.dcattr_add('tag', name, comment)
