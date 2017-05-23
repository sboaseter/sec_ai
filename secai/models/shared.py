from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#print('database_uri')
#print(config['DATABASE_URI'])
engine = create_engine('mysql+pymysql://sboa:depoi34@localhost/secai', convert_unicode=True)
db = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db.query_property()

def init_db():
	from secai.models.dbmodels import Company, Submission
