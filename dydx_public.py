
###################
## Load packages ##
###################
from web3 import Web3
from dydx3 import Client
from dydx3.modules import private, public
from dydx3.helpers.request_helpers import generate_query_path
from dydx3.helpers.requests import request
from dydx3.constants import MARKET_BTC_USD
import requests
import json
import pandas as pd
import numpy as np

######################################
## Functions not in dydx3 public.py ##
######################################
class myPublic(object):

    def __init__(
        self,
        host,
    ):
        self.host = host

    ## Request Helpers

    def _get(self, request_path, params={}):
        return request(
            generate_query_path(self.host + request_path, params),
            'get',
        )

    def _put(self, endpoint, data):
        return request(
            self.host + '/v3/' + endpoint,
            'put',
            {},
            data,
        )

    ## Requests Data
    

    def get_leaderboard(self, period="DAILY", startingBeforeOrAt=None, sortBy='PERCENT', limit='10'):
        uri = '/'.join(['/v3/leaderboard-pnl'])
        return self._get(uri,{'period': period,'startingBeforeOrAt': startingBeforeOrAt, 'sortBy': sortBy, 'limit': limit},).data 

    def get_current_hedgies(self):
        uri = '/'.join(['/v3/hedgies/current'])
        return self._get(uri).data
    
    def get_hist_hedgies(self, nftRevealType="Day", start=None, end=None):
        uri = '/'.join(['/v3/hedgies/history'])
        return self._get(uri,{'nftRevealType': nftRevealType,'start': start, 'end': end},).data 
   
    def get_insurance_fund_balance(self):
        uri = '/'.join(['/v3/insurance-fund/balance'])
        return self._get(uri).data


#######################
## Public api client ##
#######################
client = Client(host = "https://api.dydx.exchange")

## For functions not in dydx-v3-python
myclient = myPublic(host="https://api.dydx.exchange")


#################
## Get Markets ##
#################
## Get all markets
markets = client.public.get_markets()
markets = pd.DataFrame(markets.data['markets'])


####################
## Get Order Book ##
####################
## Returns the active orderbook for a market. All bids and asks that are fillable are returned.

orderbook = client.public.get_orderbook(market='BTC-USD')
ask = pd.DataFrame(orderbook.data['asks'])
bid = pd.DataFrame(orderbook.data['bids'])


################
## Get Trades ##
################
## Get trades from a market
all_trades = client.public.get_trades(market='BTC-USD',)
all_trades = pd.DataFrame(all_trades.data['trades'])

########################
## Get Fast Withdrawl ##
########################
fast_withdrawals_info = client.public.get_fast_withdrawal()
fast_withdrawals_info = pd.DataFrame(fast_withdrawals_info.data['liquidityProviders'])

######################
## Get Market Stats ##
######################
## Get an individual market's statistics over a set period of time or all available periods of time.
## Specified day range for the statistics to have been compiled over. Can be one of 1, 7, 30. Defaults to 1.

stats = client.public.get_stats(
    market=MARKET_BTC_USD,
    days=7, ## 1, 7, 30
)
stats = pd.DataFrame(stats.data['markets'])


############################
## Get Historical Funding ##
############################
## Get the historical funding rates for a market.
historical_funding = client.public.get_historical_funding(
  market='BTC-USD',
)

historical_funding = pd.DataFrame(historical_funding.data['historicalFunding'])

#################
## Get Candles ##
#################
candles = client.public.get_candles(
  market='BTC-USD',
  resolution='1DAY', ## 1DAY, 4HOURS, 1HOUR, 30MINS, 15MINS, 5MINS, 1MIN
)
candles = pd.DataFrame(candles.data['candles'])

#######################
## Get Configuration ##
#######################
## Get any global configuration variables for the exchange as a whole.
config = client.public.get_config()
config = pd.DataFrame(config.data)

###########################
## Check User & Username ##
###########################
user_exists = client.public.check_if_user_exists(
  ethereum_address='foo',
)
user_exists = pd.DataFrame([user_exists.data])

username_exists = client.public.check_if_username_exists(
  username='username',
)
username_exists = pd.DataFrame([username_exists.data])

##############
## Get Time ##
##############
time_object = client.public.get_time()
time_object = pd.DataFrame([time_object.data])


#####################
## Get Leaderboard ##
#####################
## Get the top PNLs for a specified period and how they rank against each other.
leader = myclient.get_leaderboard(period="DAILY", startingBeforeOrAt=None, sortBy='PERCENT', limit='10')
leader = pd.DataFrame(leader['topPnls'])

########################
## Get Mining Rewards ##
########################

rewards = client.public.get_public_retroactive_mining_rewards(
  ethereum_address='foo',
)
rewards = pd.DataFrame([rewards.data])


#################
## Get Hedgies ##
#################
## Get the currently revealed Hedgies for competition distribution.
hedgies = myclient.get_current_hedgies()
h_daily = pd.DataFrame(hedgies['daily'])
h_weekly = pd.DataFrame(hedgies['weekly'])


## Get the historically revealed Hedgies from competition distributions.
hist_hedgies_d = myclient.get_hist_hedgies(nftRevealType="daily")
hh_daily = pd.DataFrame(hist_hedgies_d['historicalTokenIds'])

hist_hedgies_w = myclient.get_hist_hedgies(nftRevealType="weekly")
hh_weekly = pd.DataFrame(hist_hedgies_w['historicalTokenIds'])

################################
## Get Insurance Fund Balance ##
################################
balance = myclient.get_insurance_fund_balance()
balance = pd.DataFrame([balance])

#################
## Output data ##
#################
# with pd.ExcelWriter('dydx_data.xlsx') as writer:  
#     markets.to_excel(writer, sheet_name='market') 
#     bid.to_excel(writer, sheet_name='bid')
#     ask.to_excel(writer, sheet_name='ask')
#     trade.to_excel(writer, sheet_name='trade')
#     s_trade.to_excel(writer, sheet_name='single_trade')
#     stats.to_excel(writer, sheet_name='market_stats')
#     funding.to_excel(writer, sheet_name='funding_rate')
#     config.to_excel(writer, sheet_name='config')    
#     leader.to_excel(writer, sheet_name='leaderboard')
#     h_daily.to_excel(writer, sheet_name='hedgies_daily')
#     h_weekly.to_excel(writer, sheet_name='hedgies_weekly')
#     hh_daily.to_excel(writer, sheet_name='hedgies_daily_hist')
#     hh_weekly.to_excel(writer, sheet_name='hedgies_weekly_hist')
