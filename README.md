# dchains
Document Chains, is (or will be) an easy to use scaleable electronical signed Document Management System

Document Chains manages all your Static documents, like birth certificates and bills. 
It can be uses much like GIT on a stand alone. 

It attaches documens together so they can build chains. For example: Latex results in dvi -> ps -> pdf or an RFC822 message has an attachment which is a signed pdf which contains a bill of some sort which results in a Book record. 

All this is searchable.

You can copy together two different storage pools and continue working. 

You can sign every message tag and every property. 

You can also do automatic OCR and perform tasks on various uploads. 


How will it work: 

The repo demonstration script that shows how data will be organized on the system, however there are some more proof of concepts lying around here. In general a File is saved with its SHA256sum as filename in a folder with that Checksum and at least one Gnupg Signature next to it in a seperate file. 

The same directory houses gpg signed yaml files that collect attributes like tags, mime type, common names and attachments. An attribute file can also be revoked. 

