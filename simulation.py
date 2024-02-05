# 
#   Made to RUN SIMULATIONS on my strategy before I use actual money
#
#   Look at the Logic you and isaac made in the green notebook along with the flashcards if you need any help on this
#
from time import sleep
import coinbase
import htx
import phemex
open("trades_Made.txt", "x")

###### VARIABLES ############################
phemexBalanceUSD = 100.0
phemexBalanceBTC = 0.0
htxBalanceUSD = 100.0
htxBalanceBTC = 0.0


initialMargin = 0.0
borrowed_USD = 0.0 # a.k.a. the amount earned from short selling before prices merge
BTCDebt = 0.0
BTCBought = 0.0

canPlaceOrder = True

htx_ShortSold = False
phemex_ShortSold = False

tickPricesJSON = {}
f = open("trades_Made.txt", "a")

###### FUNCTIONS ################################

def returnTickPrices():
    htxTicker = htx.getTickerPrice("btcusdt")
    phemexTicker = phemex.getTickerPrice("BTCUSDT")
    # print("HTX btcusdt: "+ str(htxTicker) +"   Phemex BTCUSDT: "+ str(phemexTicker))
    return {"htx": htxTicker, "phemex": phemexTicker}

def checkPercentageGain(tickPrices):
    percent = abs(float(((float(tickPrices['htx']) - tickPrices['phemex']) * 100) / tickPrices['phemex']))
    return percent

def calcBTCDebt(quoteQTY, maxTickPrice):
    BTCDebt = quoteQTY/maxTickPrice
    return BTCDebt

def calcBTCToBuy(quoteQTY, minTickPrice):
    BTCBought = quoteQTY/minTickPrice
    return BTCBought



##### MAIN SCRIPT ###################################


while True:
    tickPricesJSON = returnTickPrices()
    # print("ran through tick prices!!!")
    htx_BTCUSDT_Ticker = tickPricesJSON['htx']
    phemex_BTCUSDT_Ticker = tickPricesJSON['phemex']
    
    #   SCENARIO 1:
    #       HTX Ticker Price and Phemex Ticker Price are within $4 of each other
    if abs(htx_BTCUSDT_Ticker - phemex_BTCUSDT_Ticker) <= 4.0 and not canPlaceOrder:
        # figure out which exchanges you need to pay off the margin and sell off your BTC
        # start which checking which account has BTC in it and going off of that
        
        # until that I figure out how to do that,  I will just have 2 if statements for now because of the 2 situations possible
        if htx_ShortSold:
            # pay off your BTCDebt and figure out how much USD will be deposited into account (along with any fees)
            # print('\nhtx_ShortSold == True..... This means to REPAY back your BTCDEBT on HTX')
            # print('It also means to SELL your BTC on PHEMEX')
            print("\nHTX Ticker Price: " +str(htx_BTCUSDT_Ticker)+ " | Phemex Ticker Price: " +str(phemex_BTCUSDT_Ticker)+ "\n")
            f.write("\nHTX Ticker Price: " +str(htx_BTCUSDT_Ticker)+ " | Phemex Ticker Price: " +str(phemex_BTCUSDT_Ticker)+ "\n")
            # Calculate how much your BTCDebt is worth now --> converted_Debt
            converted_Debt = BTCDebt * htx_BTCUSDT_Ticker
            f.write("BTC Debt: " +str(BTCDebt))
            f.write("\nConverted Debt: " +str(converted_Debt))
            f.write("\nBorrowed USD: " +str(borrowed_USD))
            # if converted_Debt is less than the USD you got from the short sell then 
            if converted_Debt <= borrowed_USD:
                # calculate profit by subtracting the debt in USD from the USD you got from the short sell (the result is what is leftover after the debt is paid off)
                # (IF RESULT IS NEGATIVE, YOU FUCKED UP BIG TIME BRO)
                actual_Profit = borrowed_USD - converted_Debt
                f.write("\nactual_Profit: " +str(actual_Profit))
                # add your initialMargin and actual_Profit into your HTXBalanceUSD
                htxBalanceUSD += initialMargin + actual_Profit
                f.write("\nInitial Margin: " +str(initialMargin))
                # now make initialMargin = 0, borrowed_USD = 0, and BTCDebt = 0
                initialMargin = borrowed_USD = BTCDebt = 0
            
            # else if converted_Debt is more than the USD you got from the short sell then
            elif converted_Debt > borrowed_USD:
                # remaining_Debt = converted_Debt - borrowed_USD
                remaining_Debt = converted_Debt - borrowed_USD
                borrowed_USD = 0 # since you just used it to pay off part of the debt
                # initialMargin -= remaining_Debt (Yes the actual initialMargin variable this time)
                initialMargin -= remaining_Debt
                # then add the initialMargin amount into HTXBalanceUSD (whatever is leftover anyway)
                htxBalanceUSD += initialMargin
                # make BTCDebt = 0, initialMargin = 0 (because we just payed back the debt)
                BTCDebt = initialMargin = 0
                
            
            # SELLING YOUR BTC
            # calculate how much your BTCBought is worth in USD --> converted_BTCBought
            converted_BTCBought = BTCBought * phemex_BTCUSDT_Ticker
            # add converted_BTCBought to phemexBalanceUSD
            phemexBalanceUSD += converted_BTCBought
            # make BTCBought = 0, phemexBalanceBTC = 0
            phemexBalanceBTC = BTCBought = 0
            
            htx_ShortSold = False
        
        elif phemex_ShortSold:
            # pay off your BTCDebt and figure out how much USD will be deposited into account (along with any fees)
            # print('\nphemex_ShortSold == True..... This means to REPAY back your BTCDEBT on PHEMEX')
            # print('It also means to SELL your BTC on HTX')
            print("\nHTX Ticker Price: " +str(htx_BTCUSDT_Ticker)+ " | Phemex Ticker Price: " +str(phemex_BTCUSDT_Ticker)+ "\n")
            f.write("\nHTX Ticker Price: " +str(htx_BTCUSDT_Ticker)+ " | Phemex Ticker Price: " +str(phemex_BTCUSDT_Ticker)+ "\n")  
            
            # Calculate how much your BTCDebt is worth now --> converted_Debt
            converted_Debt = BTCDebt * phemex_BTCUSDT_Ticker
            print("BTC Debt: " +str(BTCDebt))
            print("Converted Debt: " +str(converted_Debt))
            print("Borrowed USD: " +str(borrowed_USD))
            f.write("BTC Debt: " +str(BTCDebt))
            f.write("\nConverted Debt: " +str(converted_Debt))
            f.write("\nBorrowed USD: " +str(borrowed_USD))
            # if converted_Debt is less than the USD you got from the short sell then 
            if converted_Debt <= borrowed_USD:
                # calculate profit by subtracting the debt in USD from the USD you got from the short sell (the result is what is leftover after the debt is paid off)
                # (IF RESULT IS NEGATIVE, YOU FUCKED UP BIG TIME BRO)
                actual_Profit = borrowed_USD - converted_Debt
                print("actual_Profit: " +str(actual_Profit))
                f.write("\nactual_Profit: " +str(actual_Profit))
                # add your initialMargin and actual_Profit into your HTXBalanceUSD
                
                
                # ALL THATS LEFT TO DO NOW IS TO CHECK trades_Made.txt AND MAKE SURE EVERY TRADE THERE IS GOOD AND WITHOUT PROBLEMS
                phemexBalanceUSD += initialMargin + actual_Profit   
                print("Initial Margin: " +str(initialMargin))
                f.write("\nInitial Margin: " +str(initialMargin))
                
                # now make initialMargin = 0, borrowed_USD = 0, and BTCDebt = 0
                initialMargin = borrowed_USD = BTCDebt = 0
                print("\nAFTER BEING SET TO ZERO")
                print("Initial Margin: " +str(initialMargin))
                print("Borrowed USD: " +str(borrowed_USD))
                print("BTC Debt: " +str(BTCDebt))
            
            # else if converted_Debt is more than the USD you got from the short sell then
            elif converted_Debt > borrowed_USD:
                # remaining_Debt = converted_Debt - borrowed_USD
                remaining_Debt = converted_Debt - borrowed_USD
                borrowed_USD = 0 # since you just used it to pay off part of the debt
                # initialMargin -= remaining_Debt (Yes the actual initialMargin variable this time)
                initialMargin -= remaining_Debt
                # then add the initialMargin amount into HTXBalanceUSD (whatever is leftover anyway)
                phemexBalanceUSD += initialMargin
                # make BTCDebt = 0, initialMargin = 0 (because we just payed back the debt)
                BTCDebt = initialMargin = 0
                
            
            # SELLING YOUR BTC
            # calculate how much your BTCBought is worth in USD --> converted_BTCBought
            converted_BTCBought = BTCBought * htx_BTCUSDT_Ticker
            # add converted_BTCBought to phemexBalanceUSD
            htxBalanceUSD += converted_BTCBought
            # make BTCBought = 0, phemexBalanceBTC = 0
            htxBalanceBTC = BTCBought = 0
            
            phemex_ShortSold = False
        
        canPlaceOrder = True
        print("\n########### BALANCE CHECK AFTER PROFIT IS MADE ##########################")
        print("HTX Balance USD: " +str(htxBalanceUSD)+ ", HTX Balance BTC: " +str(htxBalanceBTC))
        print("PHEMEX Balance USD: " +str(phemexBalanceUSD)+ ", PHEMEX Balance BTC: " +str(phemexBalanceBTC))
        print("#########################################################################\n")
        f.write("\n########### BALANCE CHECK AFTER PROFIT IS MADE ##########################\n")
        f.write("HTX Balance USD: " +str(htxBalanceUSD)+ ", HTX Balance BTC: " +str(htxBalanceBTC)+ "\n")
        f.write("PHEMEX Balance USD: " +str(phemexBalanceUSD)+ ", PHEMEX Balance BTC: " +str(phemexBalanceBTC)+ "\n")
        f.write("#########################################################################\n")
        # sleep(1)
        # continue
            
    
    #   SCENARIO 2:
    #       HTX Ticker Price > Phemex Ticker Price
    elif htx_BTCUSDT_Ticker > phemex_BTCUSDT_Ticker and canPlaceOrder:
        # Check the percent difference between Prices and see if you CAN make any amount of money from it
        # break out of the loop if the percent value isn't to your liking
        percentDiff = checkPercentageGain(tickPricesJSON)
        if not percentDiff > 0.05: # .05% is about a $18.50 difference @ $36900 per BTC ||||| Also means that you'll gain at least $0.05 minimum @ $100
            sleep(1)
            continue
        # print("\nTIME FOR ARBITRAGE   TIME FOR ARBITRAGE  \nTIME FOR ARBITRAGE  TIME FOR ARBITRAGE")
        print("\nHTX Ticker Price: " +str(htx_BTCUSDT_Ticker)+ " | Phemex Ticker Price: " +str(phemex_BTCUSDT_Ticker)+ "\n")
        f.write("HTX Ticker Price: " +str(htx_BTCUSDT_Ticker)+ " | Phemex Ticker Price: " +str(phemex_BTCUSDT_Ticker)+ "\n")
        
        canPlaceOrder = False
        htx_ShortSold = True
        
        # Set BTCDebt to proper amount and change HTX balance to $0 but change initialMargin to amount invested
        minBalance = min(htxBalanceUSD, phemexBalanceUSD)   #minBalance is the amount to invest or borrow
        BTCDebt = calcBTCDebt(minBalance, htx_BTCUSDT_Ticker)
        borrowed_USD = minBalance
        initialMargin = minBalance # initialMargin isn't usually the same amount as borrowed_USD (just fyi for future reference)
        htxBalanceUSD -= initialMargin
        
        # Set BTCBought to correct amount, change phemex balanceUSD to $0 and phemex balanceBTC to correct amount
        BTCBought = calcBTCToBuy(minBalance, phemex_BTCUSDT_Ticker)
        phemexBalanceUSD -= minBalance 
        phemexBalanceBTC = BTCBought
        
        ##### ORDER SUCCESSFULLY PLACED #####
        print("Order Successfully Placed! || SHORT SOLD HTX ||||| BOUGHT PHEMEX\n")
        f.write("Order Successfully Placed! || SHORT SOLD HTX ||||| BOUGHT PHEMEX\n")
        # continue
    
    
    #   SCENARIO 3:
    #       Phemex Ticker Price > HTX Ticker Price
    elif phemex_BTCUSDT_Ticker > htx_BTCUSDT_Ticker  and canPlaceOrder:
        # Check the percent difference between Prices and see if you CAN make any amount of money from it
        # break out of the loop if the percent value isn't to your liking
        percentDiff = checkPercentageGain(tickPricesJSON)
        if not percentDiff > 0.05: # .05% is about a $18.50 difference @ $36900 per BTC ||||| Also means that you'll gain at least $0.05 minimum
            sleep(1)
            continue
        # print("\nTIME FOR ARBITRAGE   TIME FOR ARBITRAGE  \nTIME FOR ARBITRAGE  TIME FOR ARBITRAGE")
        print("\nHTX Ticker Price: " +str(htx_BTCUSDT_Ticker)+ " | Phemex Ticker Price: " +str(phemex_BTCUSDT_Ticker)+ "\n")
        f.write("HTX Ticker Price: " +str(htx_BTCUSDT_Ticker)+ " | Phemex Ticker Price: " +str(phemex_BTCUSDT_Ticker)+ "\n")
        
        canPlaceOrder = False
        phemex_ShortSold = True
        
        # Set BTCDebt to proper amount and change phemex balance to $0 but change initialMargin to amount invested
        minBalance = min(htxBalanceUSD, phemexBalanceUSD) #minBalance is the amount to invest or borrow
        BTCDebt = calcBTCDebt(minBalance, phemex_BTCUSDT_Ticker)
        borrowed_USD = minBalance
        initialMargin = minBalance
        phemexBalanceUSD -= minBalance
        
        # Set BTCBought to correct amount, change HTX balanceUSD to $0 and HTX balanceBTC to correct amount
        BTCBought = calcBTCToBuy(minBalance, htx_BTCUSDT_Ticker)
        htxBalanceUSD -= minBalance
        htxBalanceBTC = BTCBought
        
        ##### ORDER SUCCESSFULLY PLACED #####
        print("Order Successfully Placed! || BOUGHT HTX ||||| SHORT SOLD PHEMEX\n")
        f.write("Order Successfully Placed! || BOUGHT HTX ||||| SHORT SOLD PHEMEX\n")
        # continue
    
    sleep(1)
    # print("I slept for 1 second")
 
 
################# LOGIC REMINDERS MAINLY ABOUT MATH ##################################################
#   
# $100 @ 18040 === .0055432 BTC
# $100 @ 18000 === .0055555 BTC
#
# PERCENT DIFF === .22%
#
# ASSUMING PRICES MERGE @ $18020
# AFTER PAYING OFF DEBT TOTAL IN 1st ==== $100.12
# AFTER SELLING BOUGHT BTC TOTAL IN 2nd === $100.11
# TOTAL PROFIT === $0.23
#
# CONCLUSION --> Percent Difference is the amount of cents you will gain
