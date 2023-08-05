class http:
    _urls = {}

    def __init__(self, user_id=None, external_store_id=None, store_id=None, cash_id=None, external_pos_id=None, limit=100):

        self._urls['secure_api'] = 'https://api.mercadopago.com'
        self._urls['unsecure_api'] = 'http://api.mercadopago.com'
        self._urls['qr'] = '/instore/orders/qr/seller/collectors/' + str(user_id) + '/pos/' + str(external_pos_id) + '/qrs'

        self._urls['branch_offices'] = {
                                            'create': '/users/' + str(user_id) + '/stores',
                                            'get_limited': '/users/' + str(user_id) + '/stores/search?limit='+str(limit),
                                            'get_by_id': '/users/stores'+str(store_id),
                                            'get_by_external_id': '/users/' + str(user_id) + '/stores/search?external_id=' + str(external_store_id),
                                            'update': '/users/' + str(user_id) + '/stores/' + str(store_id),
                                            'delete': '/users/' + str(user_id) + '/stores/' + str(store_id),
                                       }

        self._urls['cashes'] = {
                                    'create': '/pos',
                                    'get': '/pos',
                                    'get_by_id': '/pos/'+str(cash_id),
                                    'get_by_external_id': '/pos?external_id='+str(external_pos_id),
                                    'update': '/pos/' + str(cash_id),
                                    'delete': '/pos/' + str(cash_id),
                                }

    def get_endpoint(self, _key, sub_key=None):

        key_path = None
        sub_key_path = None

        if(_key in self._urls):            
            if(self._urls[_key]):
                key_path = self._urls[_key]
            if(sub_key):
                sub_key_path = self._urls[_key][sub_key]
            if(sub_key_path):
                return sub_key_path
            if(key_path):
                return key_path
        else:
            return None