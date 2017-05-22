from sqlalchemy import Column, Integer, String, Text, DateTime
from secai.models.shared import Base

class Company(Base):
	__tablename__ = 'company'
	id = Column('id', Integer, primary_key=True)
	symbol = Column('symbol', String(16))
	name = Column('name', String(1024))
	cik = Column('cik', String(128))
	sic = Column('sic', String(64))
	created_on = Column('created_on', DateTime)

	def __repr__(self):
		return '{}: {}'.format(self.symbol, self.name)

class Submission(Base):
	__tablename__ = 'submission'
	id = Column('id', Integer, primary_key=True)
	companyId = Column('companyId', Integer)
	accessionNo = Column('accessionNo', String(255))
	rtype = Column('type', String(45))
	acceptedOn = Column('acceptedOn', DateTime)
	content = Column('content', Text)
	matches = Column('matches', Integer)
	sentiment = Column('sentiment', String(1024))

	def __repr__(self):
		return '{}: {}'.format(str(self.companyId), str(self.matches))

