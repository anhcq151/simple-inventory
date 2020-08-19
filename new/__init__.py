from flask import Flask
from new.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

newapp = Flask(__name__)
newapp.config.from_object(Config)
db = SQLAlchemy(newapp)
migrate = Migrate(newapp, db)

from new import new, routes, models

db.create_all()
db.session.commit()
