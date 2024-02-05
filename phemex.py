import os 
import sys
import time
import helper

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../")

from phemex2.client import Client
from phemex2.exceptions import PhemexAPIException

config = helper.read_config()
api_key = config['PHEMEX']['_DEFAULT-APIKEY_']
secret_key = config['PHEMEX']['_DEFAULT-APISECRET_']

# Create a testnet client
client = Client(api_key, secret_key, False)

def getTickerPrice(coinPair):
    """ Gets the live ticker price for a certain coin pair

    Args:
        coinPair (String): The coin pair you want the price of

    Returns:
        int: The last ticker price
    """
    jsonResp = client.query_24h_ticker(coinPair)
    # have to divide twice here for some weird reason or it won't scale down???????
    lastTick = float(jsonResp['result']['lastEp'])/10000
    return lastTick/10000.0

def getBalance(currency):
    """ Gets the account balance of a currency you have

    Args:
        currency (String): The type of wallet that you want to view the balance of

    Returns:
        String: The Amount of currency you currently have in an account
    """
    jsonResp = client.query_account_n_positions(currency)
    return jsonResp['data']['account']['accountBalanceEv']