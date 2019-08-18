from flask import request, json, Response, Blueprint, g
from ..models.CustomerModel import CustomerModel, CustomerSchema
from ..shared.Authentication import Auth

customer_api = Blueprint('customer_api', __name__)
customer_schema = CustomerSchema()

@customer_api.route('/', methods=['POST'])
def create():
  req_data = request.get_json()
  data, error = customer_schema.load(req_data)

  if error:
    return custom_response(error, 400)
  
  customer_in_db = CustomerModel.get_customer_by_email(data.get('email'))
  if customer_in_db:
    message = {'error': 'Customer already exist, please supply another email address'}
    return custom_response(message, 400)
  
  customer = CustomerModel(data)
  customer.save()
  ser_data = customer_schema.dump(customer).data
  token = Auth.generate_token(ser_data.get('id'))
  return custom_response({'jwt_token': token}, 201)

@customer_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  customers = CustomerModel.get_all_customers()
  ser_customers = customer_schema.dump(customers, many=True).data
  return custom_response(ser_customers, 200)

@customer_api.route('/<int:customer_id>', methods=['GET'])
@Auth.auth_required
def get_a_customer(customer_id):
  customer = CustomerModel.get_one_customer(customer_id)
  if not customer:
    return custom_response({'error': 'customer not found'}, 404)
  
  ser_customer = customer_schema.dump(customer).data
  return custom_response(ser_customer, 200)

@customer_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
  req_data = request.get_json()
  data, error = customer_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)

  customer = CustomerModel.get_one_customer(g.customer.get('id'))
  customer.update(data)
  ser_customer = customer_schema.dump(customer).data
  return custom_response(ser_customer, 200)

@customer_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  customer = CustomerModel.get_one_customer(g.customer.get('id'))
  customer.delete()
  return custom_response({'message': 'deleted'}, 204)

@customer_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  customer = CustomerModel.get_one_customer(g.customer.get('id'))
  ser_customer = customer_schema.dump(customer).data
  return custom_response(ser_customer, 200)


@customer_api.route('/list', methods=['POST'])
@Auth.auth_required
def get_list():
  req_data = request.get_json()
  if 'n' not in req_data.keys():
    return custom_response({'error': 'value of n is required'}, 404)
  customers = CustomerModel.get_n_youngest_customers(req_data['n'])
  ser_customers = customer_schema.dump(customers, many=True).data
  return custom_response(ser_customers, 200)


@customer_api.route('/login', methods=['POST'])
def login():
  req_data = request.get_json()

  data, error = customer_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  customer = CustomerModel.get_customer_by_email(data.get('email'))
  if not customer:
    return custom_response({'error': 'invalid credentials'}, 400)
  if not customer.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 400)
  ser_data = customer_schema.dump(customer).data
  token = Auth.generate_token(ser_data.get('id'))
  return custom_response({'jwt_token': token}, 200)

  

def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
