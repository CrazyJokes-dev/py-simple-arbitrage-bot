import urllib.parse
import hashlib
import hmac
import base64
import requests
import time
import helper

config = helper.read_config()

api_url = "https://api.binance.us"

###########################################################################################

api_key = config['BINANCE']['_APIKEY_']
secret_key = config['BINANCE']['_APISECRET_']

# get binanceus signature
def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac

# Attaches auth headers and returns results of a POST request
def binanceus_request(endPoint, data, api_key, api_sec):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, api_sec)
    params={
        **data,
        "signature": signature,
        }
    req = requests.get((api_url + endPoint), params=params, headers=headers)
    return req.json()
    # return req.text

#############################################################################################


def getTickerPrice(coinPair):
    """ A function that will return the live ticker price of the coin pair specified

    Args:
        coinPair (String): a coin pair avaliable on binance.us

    Returns:
        Integer: The price of the coin pair you provided
    """
    resp = requests.get('https://api.binance.us/api/v3/ticker/price?symbol='+coinPair)
    return resp.json()['price']

def getBalance(coin):
    """ This function returns the balance of a cryptocurrency of your choice from your account

    Args:
        coin (String): the cryptocurrency balance you want to check

    Returns:
        Dictionary: free => the amount of currency avaliable to spend, locked => the amount of currency currently not available at the moment
    """
    endPoint = "/api/v3/account"
    data = {
        "timestamp": int(round(time.time() * 1000)),
    }

    get_account_result = binanceus_request(endPoint, data, api_key, secret_key)
    for key in get_account_result['balances']:
        if key['asset'] == coin:
            return {'free': key['free'], 'locked': key['locked']}
        
def createOrder(pairSymbol, side, type, quoteOrderQty):
    """This function will send a POST request so that you can buy or sell a crypto currency (aka. a coin pair)

    Args:
        pairSymbol (String): Order Trading Pair (e.g., BTCUSDT, ETHUSDT)
        side (String): Order side (e.g., BUY, SELL)
        type (String): Order type (e.g., LIMIT, MARKET, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER)
        quoteOrderQty (Integer): MARKET orders using **quoteOrderQty** specify the amount the user wants to SPEND when BUYING or RECEIVE when SELLING the quote asset
        
    Returns:
        String: The original ClientOrderID created for this order just in case we need to check the trade order status using **Get Order API CALL**
    """
    endPoint = "/api/v3/order/test"
    data = {
        "symbol": pairSymbol,
        "side": side,
        "type": type,
        "quoteOrderQty": quoteOrderQty,
        "timestamp": int(round(time.time() * 1000))
    }

    result = binanceus_request(endPoint, data, api_key, secret_key)
    # print(result['clientOrderId'])
    return result['clientOrderId']