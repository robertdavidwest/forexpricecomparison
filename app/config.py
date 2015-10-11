# config.py
import os

CSRF_ENABLED = True
SECRET_KEY = 'TEST123'
flavor = 'mysql'

if flavor == 'sqlite':
    # grab the folder where the script runs
    basedir = os.path.abspath(os.path.dirname(__file__))

    DATABASE = 'fx_quotes.db'

    # the full database path
    DATABASE_PATH = os.path.join(basedir, DATABASE)

    # the database uri
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

elif flavor == 'mysql':

    # settings for pythonanywhere mysql database #
    DATABASE = 'robertdavidwest$fx_quotes'
    HOSTNAME = 'robertdavidwest.mysql.pythonanywhere-services.com'
    USERNAME = 'robertdavidwest'
    MYSQL_PASSWORD = 'test'

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}/{}'.format(USERNAME,
                                                                   MYSQL_PASSWORD,
                                                                   HOSTNAME,
                                                                   DATABASE)

    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://robertdavidwest:test@robertdavidwest.mysql.pythonanywhere-services.com/robertdavidwest$fx_quotes'