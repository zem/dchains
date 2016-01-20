# all database table definitions will go here 
import datetime
import sqlalchemy
from lbledger import *
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from sqlalchemy import UniqueConstraint, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import Currency
#alchemys engine creation
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DcIdx = declarative_base()

#__all__=['Account', 'AccountTags', 'Transaction', 'Accounting', 'ChangeLog', 'Template', 'LblBase']

class DcAttr(DcIdx):
	__tablename__ = 'dcattrs'
	
	tagid = Column(String(64), ForeignKey('document.id'), primary_key=True)
	docid = Column(String(64), ForeignKey('document.id'), nullable=False)
	key = Column(String, nullable=False)
	value = Column(String, nullable=False)
	comment = Column(String, nullable=False)
	__table_args__ = (
		UniqueConstraint("docid", 'key', 'value'),
	);

# however this will only contain searchable content so you can do a LIKE %sth% query 
# later also a search engine will be supported 
class DcContent(DcIdx):
	__tablename__ = 'dccontent'
	
	docid = Column(String(64), ForeignKey('document.id'), primary_key=True)
	content=Column(String)


class DcDocSig(DcIdx):
	__tablename__ = 'dcsigs'
	
	docid = Column(String(64), ForeignKey('document.id'), primary_key=True)
	# all the fields needed for a signature here 
