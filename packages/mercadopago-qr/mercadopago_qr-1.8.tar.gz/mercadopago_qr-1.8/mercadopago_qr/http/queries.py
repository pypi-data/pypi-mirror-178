import json
import requests

class queries:

    def post(self, params={}):
        response = requests.post(url=params['url'], headers=params['headers'], data=json.dumps(params['data']), verify=params['verify'])
        return response
    
    def get(self, params={}):
        response = requests.get(url=params['url'], headers=params['headers'], data=json.dumps(params['data']), verify=params['verify'])
        return response

    def put(self, params={}):
        response = requests.put(url=params['url'], headers=params['headers'], data=json.dumps(params['data']), verify=params['verify'])
        return response
    
    def delete(self, params={}):
        response = requests.delete(url=params['url'], headers=params['headers'], data=json.dumps(params['data']), verify=params['verify'])
        return response
    
    def get_headers_qr(self, server):
        _headers = {}
        _headers['Authorization'] = str(
            "Bearer") + str(" ") + str(server.client_secret)
        _headers['Accept'] = 'application/json'
        if(server.client_id):
            _headers['client_id'] = server.client_id
        if(server.client_secret):
            _headers['client_secret'] = server.client_secret
        if(server.client_id):
            _headers['client_id'] = server.client_id
        return _headers
    
    def get_headers_branch_offices(self, server):
        _headers = {}
        _headers['Authorization'] = str(
            "Bearer") + str(" ") + str(server.client_secret)
        _headers['Accept'] = 'application/json'
        if(server.client_id):
            _headers['client_id'] = server.client_id
        if(server.client_secret):
            _headers['client_secret'] = server.client_secret
        if(server.client_id):
            _headers['client_id'] = server.client_id
        return        
    
    def get_headers_cashes(self, server):
        _headers = {}
        _headers['Authorization'] = str(
            "Bearer") + str(" ") + str(server.client_secret)
        _headers['Accept'] = 'application/json'
        if(server.client_id):
            _headers['client_id'] = server.client_id
        if(server.client_secret):
            _headers['client_secret'] = server.client_secret
        if(server.client_id):
            _headers['client_id'] = server.client_id
        return _headers