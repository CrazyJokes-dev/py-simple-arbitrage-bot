import requests
from requests.auth import AuthBase
import hmac
import hashlib
import time
import json
import time
import helper

config = helper.read_config()

api_url = "https://api.coinbase.com"

###########################################################################################

api_key = config['COINBASE']['_APIKEY_']
secret_key = config['COINBASE']['_APISECRET_']

class CBAuth(AuthBase):

    def __init__(self, secret_key, api_key, endPoint):
        # setup any auth-related data here
        self.secret_key = secret_key
        self.api_key = api_key
        self.api_url = endPoint
        # print(secret_key, api_key, api_url)

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url.split('?')[0] + str(request.body or '')
        signature = hmac.new(self.secret_key.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

        request.headers.update({
            'CB-ACCESS-SIGN': str(signature.hex()),
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'Content-Type': "application/json"
        })
        # print(message, '<--- MESSAGE!!!!')
        # print(request.headers)
        return request

# endPoint = '/api/v3/brokerage/accounts/80a4079d-1093-568c-9b90-005da946a4c5'
# payload = {
#     # Body Params go here
# }
# auth = CBAuth(secret_key, api_key, endPoint)
# r = requests.get(api_url + endPoint, params=payload, auth=auth).json()
# print(str(r))

#############################################################################################

def getTickerPrice(coinPair):
    """ A function that will return the live ticker price of the coin pair specified

    Args:
        coinPair (String): The trading pair, i.e., 'BTC-USD'.
        limit (Integer): Number of trades to return.

    Returns:
        Integer: The price of the trading pair you provided
    """
    # This endpoint requires no request body(aka payload) so payload will be empty and that is fine for GET requests
    endPoint = "/api/v3/brokerage/products/"+coinPair
    payload = {
    # Body Params go here
    }
    auth = CBAuth(secret_key, api_key, endPoint)
    resp = requests.get(api_url + endPoint, params=payload, auth=auth).json()
    return resp['price']

def getAccountBalance(currency):
    endPointUSD = "/api/v3/brokerage/accounts/ac19b7e4-1e48-5b83-8afb-599e404c3444"
    endPointBTC = "/api/v3/brokerage/accounts/80a4079d-1093-568c-9b90-005da946a4c5"
    
    if currency == 'USD':
        auth = CBAuth(secret_key, api_key, endPointUSD)
        resp = requests.get(api_url + endPointUSD, auth=auth).json()
    elif currency == 'BTC':
        auth = CBAuth(secret_key, api_key, endPointBTC)
        resp = requests.get(api_url + endPointBTC, auth=auth).json()
        
    return resp['account']['available_balance']['value']