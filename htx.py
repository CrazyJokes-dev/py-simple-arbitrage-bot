from huobi.client.account import AccountClient
from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.utils import *

import helper
config = helper.read_config()
api_key = config['HTX']['_APIKEY_']
secret_key = config['HTX']['_APISECRET_']
account_id1 = 59775009

market_client = MarketClient()
account_client = AccountClient(api_key=api_key, secret_key=secret_key)




#   ALL COIN PAIRS HAVE TO BE LOWERCASE OR THE CODE WON'T WORK!!!!!
#   ALL COIN PAIRS HAVE TO BE LOWERCASE OR THE CODE WON'T WORK!!!!!
#   ALL COIN PAIRS HAVE TO BE LOWERCASE OR THE CODE WON'T WORK!!!!!
def getTickerPrice(coinPair):
    """ Gets the current live ticker price for a coin pair
    
    Args:
        coinPair (String): MUST BE IN LOWERCASE!!! The coin pair ticker price you want to see. MUST BE IN LOWERCASE!!!

    Returns:
        float: the ticker price for your selected coin pair
    """
    obj = market_client.get_market_detail_merged(coinPair)
    members = [attr for attr in dir(obj) if not callable(attr) and not attr.startswith("__")] # Turns the Object into a list that we can read the values in
    for member_def in members: # member_def = parameter name, val_str = value of parameter
        val_str = str(getattr(obj, member_def))
        if member_def == 'close':
            return float(val_str)
        
def getBalance(currency=str):
    """ Retrieves the balance from your HTX account

    Args:
        currency (String): the crypto balance you want to retrieve

    Returns:
        float(decimal): the balance of the selected crypto in your account
    """
    account_balance_list = account_client.get_account_balance()
    if account_balance_list and len(account_balance_list):
        for account_balance_obj in account_balance_list:
            if account_balance_obj and len(account_balance_obj.list):
                for balance_obj in account_balance_obj.list:
                    if (balance_obj.currency == currency) and balance_obj.type == "trade":
                        return float(balance_obj.balance)


# WORK ON GETTING THE BALANCE OF YOUR ACCOUNT
# THEN FINISH THE MAIN SCRIPT OF YOUR SIMULATION.PY