#!/usr/bin/python3
import dchain.dcdoc

doc=dchain.dcdoc(filename="README.md")
doc.save_all()
doc.add_name("README.md")
doc.add_tag("TestFile")

