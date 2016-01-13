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
from datetime import datetime

"""
class dcdoc()
===========

"""
class doc():
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
	- docid: the document id (sha256 hexadecimal checksum over the content)
	- keyid: which keyid should be used to sign documents and attachments
	- storebase: The directory where the document chains storage is located
	- gpgbin: defaults to gpg2
	"""
	def __init__(self, filename='', docid='', content='',
		contenttype='', 
		keyid='',
		storebase=os.environ["HOME"]+"/.dchains/",
		gpgbin='gpg2',
	):
		# copy all that neccessary stuff to self
		self.path=path
		self.filename=filename
		self.docid=docid
		self.contenttype=contenttype
		self.dcattrs=[]
		self.revoked_dcattrs={}
		self.dcattr_by_name={}
		self.dcattr_by_id={}
		self.keyid=keyid
		self.storebase=storebase
		self.gpgbin=gpgbin
		self.gpg=gnupg.GPG(gpgbinary=gpgbin)
		self.sha=hashlib.sha256()
		# we implement three modes , 
		# only a document id 
		# only a filename 
		# content and a filename given
		# there is something odd if we have both or none 
		#  at initialization
		if docid=="" and fileaname=="" and content=="": 
			raise Exception("please set either content or docid or give a filename to load")
		
		if docid!="" and fileaname!="": 
			raise Exception("filename and docid was given")
		
		if docid!="" and content!="": 
			raise Exception("content and docid was given")
		
		if filename!="" and content!="": 
			raise Exception("content and filename was given")
	
		if docid!='':
			self._load_docid(docid)
		elif filename!='';
			self._load_filename(filename)
		elif content!='';
			self._load_content(content)

	"""
	store
	-----
	stores the document and to the storage, or updates the stored document 
	in the storage
	"""
	def save_all(self):
		self.save_content()
		self.sign()
		#self.save_attributes()

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
	def _load_filename(self, filename)
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
		sha.update(content)
		if self.docid=='':
			self.docid=sha.hexdigest()
		elif self.docid != sha.hexdigest():
			raise Exception("uuups, we loaded a document to the content but its checksum does not match our docid")
		
		# TODO as soon as I have the attributes ready, 
		# we make an attribute detection here
		
	def _load_docid(self, docid):
		# there is not yet anything to do here yet 
		# but to raise an exception if the document is not in the pool
		if not os.path.exists(self.contentfile()):
			raise Exception("this document ".self.contentfile()." does not exists in dchains storage")
		# TODO load attributes to object
	def _load_dcattrs(self):
		# as soon as we have a docid we also have workdir()
		for dcattr_file in os.listdir(self.workdir())
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
	def _detect_content_type(self):
		# we need that later, but i guess we might 
		# move that also then 
		if self.content == '':
			raise Exception("I have no content stored in the object")
		if self.contenttype == '':
			self.mime = magic.open(magic.MAGIC_MIME) 
			self.mime.load()
			self.contenttype=mime.buffer(content) 
	def _require_memory_content(self):
		if self.content=="":
			self._load_filename(self.contentfile())
	def workdir(self):
		if self.docid == '':
			raise Exception("no docid which is needed to create the docdir/workdir")
		if not self.docdir:
			self.docdir=chksum[0:8]+"/"+chksum[8:16]+"/"+chksum[16:24]+"/"+chksum
		workdir=self.storebase+self.docdir
		if not os.path.isdir(workdir):
			os.makedirs(workdir)
		return(workdir)
	def contentfile(self):
		return(self.workdir()+"/"+self.docid+".dat")
	def sign(self):
		sigfile=self.workdir()+"/"+self.docid+"_"+self.keyid+".gpg"
		if os.path.exists(sigfile):
			raise Exception("signature "+sigfile+" is already there")
		self._require_memory_content()
		signature=self.gpg.sign(self.content, 
			detach=True, 
			binary=True, 
			keyid=self.keyid
		)
		f=open(sigfile, "wb")
		f.write(signature.data)
		f.close()
	def dcattr_values_dict(self, name):
		names={}
		for a in self.dcattr_by_name[name]:
			if not a.value() in names:
				names[a.value()]=a
		return(names)
	def dcattr_values(self, name):
		return(self.dcattr_values_dict(name).keys())
