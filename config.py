import sys
class Config(object):
#	DEBUG = False
	TESTING = False
#	SQLALCHEMY_DATABASE_URI = ''
#	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = '\x96}\xdeMcx\xdb7Xa\x95A\x1f\xd4\xff>\n`\xf0\x08\x0f\xc9\xef\xe9'
	DATABASE_URI = 'mysql+pymysql://sboa:depoi34@localhost/sec8k'
	if sys.platform == 'linux2':
		APPUSER = 'rain'
		SCRIPT_DIR = '/public_html/rain/scripts/'
	if sys.platform == 'win32':
		APPUSER = 'DESKTOP-6FNTUGR\\Sigurd'
		SCRIPT_DIR = '\\scripts\\'
	#EXPLAIN_TEMPLATE_LOADING =  True

class ProductionConfig(Config):
#	print 'ProductionConfig loaded\n'
	#SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://twitterbot:stacked!123@localhost/iflychatbot'
	DEBUG = False


class DevelopmentConfig(Config):
	DEBUG = True
#	SQLALCHEMY_DATABASE_URI = ''

#class StandaloneConfig(Config):
#	print 'StandaloneConfig loaded\n'


