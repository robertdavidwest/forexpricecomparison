# config.py
import os
import ast

CSRF_ENABLED = True
SECRET_KEY = 'TEST123'
flavor = 'mysql'

# grab the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

if flavor == 'sqlite':

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
    pwords_filename = os.path.join(basedir, 'pwords.txt')
    with open(pwords_filename, 'r') as file:
        f=file.read()


        pwords = ast.literal_eval(f)
        print pwords
        print pwords['fx_quotes']

        MYSQL_PASSWORD = pwords['fx_quotes']
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}/{}'.format(USERNAME,
                                                                   MYSQL_PASSWORD,
                                                                   HOSTNAME,
                                                                   DATABASE)
