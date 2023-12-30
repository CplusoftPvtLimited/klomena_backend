import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# environment = os.getenv('env')
#
# config = configparser.ConfigParser(interpolation=None)
# config.read('db.ini')
# config.sections()
# db_user = config[environment.upper()]['dbUser']
# db_password = config[environment.upper()]['dbPassword']
# db_host = config[environment.upper()]['dbHost']
# db_name = config[environment.upper()]['dbName']
# local db
# db_user ='postgres'
# db_password ='admin'
# db_host ='127.0.0.1'
# db_name ='klomena_db'

# staging db
db_user ='postgres'
db_password ='KlammmWttQ'
db_host ='20.174.24.35'
db_name ='klomena_database'



DATABASE_URL = "postgresql://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name)
print("DATABASE_URL", DATABASE_URL)
db_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()
