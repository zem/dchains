#!/usr/bin/python3
import hashlib
import gnupg
import sys, os
import magic
import yaml

if not 0 in sys.argv:
	print("Usage: dchain.py file Tag1 Tag2 TagN ....")
	exit(1)

if not os.path.exists(sys.argv[0]):
	print("File "+sys.argv[0]+" does not exists!")
	exit(2)

storbase=os.env["HOME"]."/.dchains/"

filepath=sys.argv[0]
tags=sys.argv[1:]

gpg=gnupg.GPG(gpgbinary='gpg2')
sha=hashlib.sha512()

f=open(sys.argv[0], "rb")
content=f.read()
f.close()
sha.update(content)
chksum=sha.hexdigest()

workdir=storbase+chksum[0:15]+"/"+chksum[16:31]+"/"+chksum[32:47]+"/"+chksum[48:63]+"/"+chksum

if not os.path.isdir(path):
	os.makedirs(path)


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

signature=gpg.sign(content, keyid=keyid, binary=True)

f=open(sigfile, "wb")
f.write(signature)
f.close()

f=open(datfile, "wb")
f.write(content)
f.close()

