#!/usr/bin/python3
import hashlib
import gnupg
import sys, os
import magic
import yaml
import re
from datetime import datetime


class dcattr()
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
		if doc=='':
			raise Exception("dcattr needs a dchains.doc object to do work")
		self.doc=doc
		if dcattrfilename!='':
			dcattrid=re.sub('\.dcattr$', '', dcattrfilename)
		if dcattrid=='':
			self.stored=False
			self.a={
				doc.docid=>{
					'name'=>name,
					'value'=>value,
					'comment'=>comment,
					'ts'=>str(ts),
				}
			}
			self.ts=ts
		else:
			self.stored=True
			self._load_dcattrid(self, dcattrid)
	def _load_dcattrid(self, dcattrid):
		self.dcattrid=dcattrid
		f=open(self.doc.workdir()+"/"+dcattrid+".dcattr", "rb")
		content=f.read()
		f.close()
		verified=self.gpg.verify(content)
		if not verified: raise Exception("Signature could not be verified!")
		sha=hashlib.sha256()
		sha.update(content)
		if sha.hexdigest() != dcattrid:
			raise Exception("checksum mismatch during load of dcattr from storage")	
		# TODO Better verification here 
		data=self.gpg.decrypt(content)
		self.a=yaml.load(data)
		if not self.doc.docid in self.a:
			raise Exception("Documentid must be stored in dataset!")	
	def save(self):
		dcattrsig=gpg.sign(yaml.dump(self.a, default_flow_style=False),
			keyid=self.doc.keyid,
		)
		sha=hashlib.sha256()
		sha.update(dcattrsig.data)
		dcattrid=sha.hexdigest()
		f=open(self.doc.workdir()+"/"+dcattrid+".dcattr", "wb")
		f.write(dcattrsig.data)
		f.close()
	def lookup(self, key):
		return self.a[self.doc.docid][key]
	def value(self):
		return self.lookup('value')
	def name(self):
		return self.lookup('name')
	def comment(self):
		return self.lookup('comment')
	def ts(self):
		return date.datetime(self.lookup('ts'))























#if not 1 in sys.argv:
#	print("Usage: dchain.py file Tag1 Tag2 TagN ....")
#	exit(1)

if not os.path.exists(sys.argv[1]):
	print("File "+sys.argv[1]+" does not exists!")
	exit(2)


storbase=os.environ["HOME"]+"/.dchains/"

filepath=sys.argv[1]
tags=sys.argv[2:]

print("adding "+filepath+" to document chains")

gpg=gnupg.GPG(gpgbinary='gpg2')
sha=hashlib.sha256()

f=open(filepath, "rb")
content=f.read()
f.close()
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

