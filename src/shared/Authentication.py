import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.CustomerModel import CustomerModel

blacklist_token = []

class Auth():
  @staticmethod
  def generate_token(customer_id):
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': customer_id
      }
      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        'HS256'
      ).decode("utf-8")
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error in generating customer token'}),
        status=400
      )

  @staticmethod
  def decode_token(token):
    re = {'data': {}, 'error': {}}
    try:
      payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
      re['data'] = {'customer_id': payload['sub']}
      return re
    except jwt.ExpiredSignatureError as e1:
      re['error'] = {'message': 'token expired, please login again'}
      return re
    except jwt.InvalidTokenError:
      re['error'] = {'message': 'Invalid token, please try again with a new token'}
      return re

  @staticmethod
  def auth_required(func):
    @wraps(func)
    def decorated_auth(*args, **kwargs):
      if 'api-token' not in request.headers:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
          status=400
        )
      token = request.headers.get('api-token')
      if token in blacklist_token:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'invalid token'}),
          status=400
        )
      data = Auth.decode_token(token)
      blacklist_token.append(token)
      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps(data['error']),
          status=400
        )
        
      customer_id = data['data']['customer_id']
      check_customer = CustomerModel.get_one_customer(customer_id)
      if not check_customer:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'customer does not exist, invalid token'}),
          status=400
        )
      g.customer = {'id': customer_id}
      return func(*args, **kwargs)
    return decorated_auth
