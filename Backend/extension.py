from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS # 跨域请求伪造

#Here you are creating an instance of the SQLAlchemy class and assigning it to the variable db.
# This instance will be used throughout your application to define and manage your models and interact with the database.
db = SQLAlchemy()
cors = CORS()

