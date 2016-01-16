# dchains
Document Chains, is (or will be) an easy to use scaleable electronical signed Document Management System

Document Chains manages all your Static documents, like birth certificates and bills. 
It can be uses much like GIT on a stand alone. 

It attaches documens together so they can build chains. For example: Latex results in dvi -> ps -> pdf or an RFC822 message has an attachment which is a signed pdf which contains a bill of some sort which results in a Book record. 

All this is searchable.

You can copy together two different storage pools and continue working. 

You can sign every message tag and every property. 

You can also do automatic OCR and perform tasks on various uploads. 


How will it work?: 

The repo demonstration script that shows how data will be organized on the system, however there are some more proof of concepts lying around here. In general a File is saved with its SHA256sum as filename in a folder with that Checksum and at least one Gnupg Signature next to it in a seperate file. 

The same directory houses gpg signed yaml files that collect attributes like tags, mime type, common names and attachments. An attribute file can also be revoked. 

Why not GIT?

Git does an amazing job for all documents that are evolving during their lifetime. But the documents in Scanned archives and Accountings are not evolving, they are much more static, a document comes in and stays there. Sometimes an OCR software runs through and produces searchable data, that needs to be attached to the originating document, pdf can do this, but there are a few others who can't. Another problem is: what happens if a signed document comes in via E-Mail? Document Chains can handle theese signatures directly. Or what if you wand to split up your Bank account download to several records, to see if one is already done?  A document exists only once in document chains, so adding the same document to the pool will just result in an added name or extra tags. You can link a document to a specific version in a git repository as well as finding similar documents via add on daemons and link those together.  git is where you create documents and dchains is where you drop them off, once you are done. 

And now back to the code.. :) 

Here is an example, it has one document already stored and then it attaches 
another document to it:

-----------------------------------

#!/usr/bin/python3
import dchain.dcdoc
import dchain.dcconf
from dchain.dcdoc import *

print("Hello")
doc=dcdoc(dcdocid="b225c5500f802a6dd29cc607fc03e9c3000804f1c7526a85d04c4a284208f9f3")
doc.add_tag("TestFileTag2")

print("Names:")
print(doc.names())
print("Tags:")
print(doc.tags())

print("Attaching dchains.py")
doc2=dcdoc(filename="dchains.py")
doc2.save_all()
doc2.add_name("dchains.py")
doc2.add_tag("ChainedDocument")
doc.add_attachment(doc2)

print("What is the name of my attachment?")
print(doc.attachments()[0].names())

------------------------------------------


