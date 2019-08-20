# src/models/CustomerModel.py
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from sqlalchemy import desc

class CustomerModel(db.Model):
  # table name
  __tablename__ = 'customers'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  dob = db.Column(db.Date)
  updated_at = db.Column(db.DateTime)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)

  # class constructor
  def __init__(self, data):
    self.name = data.get('name')
    self.dob = data.get('dob')
    self.updated_at = datetime.datetime.utcnow()
    self.email = data.get('email')
    self.password = self.__generate_hash(data.get('password'))

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      if key == 'password':
        self.password = self.__generate_hash(value)
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_n_youngest_customers(n):
    qry = CustomerModel.query.order_by(desc(CustomerModel.dob)).limit(n).all()
    return qry

  @staticmethod
  def get_all_customers():
    return CustomerModel.query.all()

  @staticmethod
  def get_one_customer(id):
    return CustomerModel.query.get(id)
  
  @staticmethod
  def get_customer_by_email(value):
    return CustomerModel.query.filter_by(email=value).first()

  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)
  
  def __repr(self):
    return '<id {}>'.format(self.id)

class CustomerSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  dob = fields.Date(required=True)
  updated_at = fields.DateTime(dump_only=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True, load_only=True)

