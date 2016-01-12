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
	def save(self):
		# store the document and all its objects 
		# to the repository
	
	"""
	_load_filename
	---------------------
	this internal method is used to load the content of a file into 
	the object to calculate its checksum. This could be a bit memory 
	intense for big documents. 
	"""
	def _load_filename(self)
		filepath=self.path+"/"+self.filename
		if not os.path.exists(filepath):
			raise Exception("File "+filepath+" does not exists!")
		f=open(filepath, "rb")
		self.content=f.read()
		f.close()
	
	"""
	_load_content_from_fs
	---------------------
	this internal method is used to load the content of a file into 
	the object to calculate its checksum. This could be a bit memory 
	intense for big documents. 
	"""
	def _detect_content_type(self)
		# we need that later, but i guess we might 
		# move that also then 
		if self.content == '':
			raise Exception("I have no content stored in the object")
		if self.contenttype == '':
			self.mime = magic.open(magic.MAGIC_MIME) 
			self.mime.load()
			self.contenttype=mime.buffer(content) 
	
	def workdir(self):
		if self.docid == '':
			raise Exception("no docid which is needed to create the docdir/workdir")
		if not self.docdir:
			self.docdir=chksum[0:8]+"/"+chksum[8:16]+"/"+chksum[16:24]+"/"+chksum
		workdir=self.storebase+self.docdir
		if not os.path.isdir(workdir):
			os.makedirs(workdir)
		return workdir






		if self.docid=="":
			sha.update(self.content)
			self.docid=sha.hexdigest()
		else:
			sha.update(self.content)
			self.docid=sha.hexdigest()


gpg=gnupg.GPG(gpgbinary='gpg2')
sha=hashlib.sha256()

sha.update(content)
chksum=sha.hexdigest()

workdir=storbase+chksum[0:8]+"/"+chksum[8:16]+"/"+chksum[16:24]+"/"+chksum

if not os.path.isdir(workdir):
	os.makedirs(workdir)


datfile=workdir+"/"+chksum+".dat"
if os.path.exists(datfile):
	print("File "+chksum+" already in document chains, we do not need to do anything")
	exit(0)

# try to detect mime type of the file 
mime = magic.open(magic.MAGIC_MIME) 
mime.load() 
mimetype=mime.buffer(content) 

keyid='FECB1F75'
sigfile=workdir+"/"+chksum+"_"+keyid+".gpg"

signature=gpg.sign(content, detach=True, binary=True, keyid=keyid)

#print(signature)
f=open(sigfile, "wb")
f.write(signature.data)
f.close()

f=open(datfile, "wb")
f.write(content)
f.close()

sigprefix=workdir+"/"
sigsuffix="_"+keyid+".sig"

def set_attr(chksum, name, val):
	foo={}
	foo[chksum]={}
	foo[chksum]["ts"]=str(datetime.utcnow())
	foo[chksum][name]=val
	attrsig=gpg.sign(yaml.dump(foo, default_flow_style=False),
		keyid=keyid,
	)
	sha=hashlib.sha256()
	sha.update(attrsig.data)
	attrchksum=sha.hexdigest()
	f=open(sigprefix+attrchksum+"_"+name+sigsuffix, "wb")
	f.write(attrsig.data)
	f.close()

print("Setting mimetype: "+mimetype)
set_attr(chksum, "mimetype", mimetype)
print("Setting name: "+os.path.basename(filepath))
set_attr(chksum, "name", os.path.basename(filepath))
for tag in tags:
	print("Setting tag: "+tag)
	set_attr(chksum, "tag", tag)

