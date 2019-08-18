from flask import Flask

from .config import app_config
from .models import db, bcrypt

from .views.CustomerView import customer_api as customer_blueprint


def create_app(env_name):
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(customer_blueprint, url_prefix='/api/v1/customers')

  return app

