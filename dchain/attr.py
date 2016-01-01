
#!/usr/bin/python3
import hashlib
import gnupg
import sys, os
import magic
import yaml
from datetime import datetime

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

