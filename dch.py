#!/usr/bin/python3
import dchain.dcdoc
import dchain.dcconf
from dchain.dcdoc import *

print("Hello")
doc=dcdoc(filename="README.md")
doc.save_all()
doc.add_name("README.md")
doc.add_tag("TestFile")

