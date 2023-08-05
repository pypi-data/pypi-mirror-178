from ..http.http import http
from ..http.server import server
from ..http.queries import queries
import qrcode
from io import BytesIO
import base64

import logging
_logger = logging.getLogger(__name__)

class cashes:

    def create(self, params={}):
        qr_request = queries()
        url = http(user_id=params['user_id'])

        endpoint = None
        if(bool(params['verify'])):
            endpoint = str(url.get_endpoint('unsecure_api')) + str(url.get_endpoint('cashes', 'create'))
        else:
            endpoint = str(url.get_endpoint('secure_api')) + str(url.get_endpoint('cashes', 'create'))
        
        mercadopago = server(client_secret=params['client_secret'])
        headers = qr_request.get_headers_cashes(mercadopago)
        params['headers'] = headers
        params['url'] = endpoint
        response = qr_request.post(params)
        
        return response
    
    def get_limited(self, params={}):
        qr_request = queries()
        url = http(user_id=params['user_id'], limit=params['limit'])

        endpoint = None
        if(bool(params['verify'])):
            endpoint = str(url.get_endpoint('unsecure_api')) + str(url.get_endpoint('cashes', 'get_limited'))
        else:
            endpoint = str(url.get_endpoint('secure_api')) + str(url.get_endpoint('cashes', 'get_limited'))
        
        mercadopago = server(client_secret=params['client_secret'])
        headers = qr_request.get_headers_cashes(mercadopago)
        params['headers'] = headers
        params['url'] = endpoint
        response = qr_request.get(params)
        
        return response
    
    def get_by_id(self, params={}):
        qr_request = queries()
        url = http(cash_id=params['store_id'])

        endpoint = None
        if(bool(params['verify'])):
            endpoint = str(url.get_endpoint('unsecure_api')) + str(url.get_endpoint('cashes', 'get_by_id'))
        else:
            endpoint = str(url.get_endpoint('secure_api')) + str(url.get_endpoint('cashes', 'get_by_id'))
        
        mercadopago = server(client_secret=params['client_secret'])
        headers = qr_request.get_headers_cashes(mercadopago)
        params['headers'] = headers
        params['url'] = endpoint
        response = qr_request.get(params)
        
        return response

    def get_by_external_id(self, params={}):
        qr_request = queries()
        url = http(external_pos_id=params['external_pos_id'])

        endpoint = None
        if(bool(params['verify'])):
            endpoint = str(url.get_endpoint('unsecure_api')) + str(url.get_endpoint('cashes', 'get_by_external_id'))
        else:
            endpoint = str(url.get_endpoint('secure_api')) + str(url.get_endpoint('cashes', 'get_by_external_id'))
        
        mercadopago = server(client_secret=params['client_secret'])
        headers = qr_request.get_headers_cashes(mercadopago)
        params['headers'] = headers
        params['url'] = endpoint
        response = qr_request.get(params)
        
        return response
    
    def update(self, params={}):
        qr_request = queries()
        url = http(external_pos_id=params['external_pos_id'])

        endpoint = None
        if(bool(params['verify'])):
            endpoint = str(url.get_endpoint('unsecure_api')) + str(url.get_endpoint('cashes', 'update'))
        else:
            endpoint = str(url.get_endpoint('secure_api')) + str(url.get_endpoint('cashes', 'update'))

        mercadopago = server(client_secret=params['client_secret'])
        headers = qr_request.get_headers_cashes(mercadopago)
        params['headers'] = headers
        params['url'] = endpoint
        response = qr_request.put(params)
        
        return response
    
    def delete(self, params={}):
        qr_request = queries()
        url = http(store_id=params['store_id'])

        endpoint = None
        if(bool(params['verify'])):
            endpoint = str(url.get_endpoint('unsecure_api')) + str(url.get_endpoint('cashes', 'delete'))
        else:
            endpoint = str(url.get_endpoint('secure_api')) + str(url.get_endpoint('cashes', 'delete'))
        
        mercadopago = server(client_secret=params['client_secret'])
        headers = qr_request.get_headers_cashes(mercadopago)
        params['headers'] = headers
        params['url'] = endpoint
        response = qr_request.delete(params)
        
        return response