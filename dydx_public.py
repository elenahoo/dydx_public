
###################
## Load packages ##
###################

from dydx3 import Client
from web3 import Web3
from dydx3.helpers.request_helpers import generate_query_path
from dydx3.helpers.requests import request
import requests
import json
import pandas as pd
import numpy as np

###################
## Define class  ##
###################
class Public(object):

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
    
    def get_market(self):
        uri = '/'.join(['/v3/markets'])
        return self._get(uri).data 
    
    def get_orderbook(self, market):
        uri = '/'.join(['/v3/orderbook', market])
        return self._get(uri).data 

     
    def get_trade(self, market, startingBeforeOrAt=None, limit=None):
        uri = '/'.join(['/v3/trades', market])
        if(startingBeforeOrAt is None or limit is None):
            uri_full = uri
        else:
            uri_full = uri + '?startingBeforeOrAt=' + startingBeforeOrAt + '&limit=' + limit
        return self._get(uri_full).data 
   

    def get_stats(self, market, days=1):
        uri = '/'.join(['/v3/stats', market])
        return self._get(uri,{'days': days},).data


    def get_historical_funding(self, market, effective_before_or_at=None):
        uri = '/'.join(['/v3/historical-funding', market])
        return self._get(uri,{'effectiveBeforeOrAt': effective_before_or_at},).data 
    
    def get_config(self):
        uri = '/'.join(['/v3/config'])
        return self._get(uri).data 

    def get_leaderboard(self, period="DAILY", startingBeforeOrAt=None, sortBy='PERCENT', limit='10'):
        uri = '/'.join(['/v3/leaderboard-pnl'])
        return self._get(uri,{'period': period,'startingBeforeOrAt': startingBeforeOrAt, 'sortBy': sortBy, 'limit': limit},).data 

    def get_current_hedgies(self):
        uri = '/'.join(['/v3/hedgies/current'])
        return self._get(uri).data
    
    def get_hist_hedgies(self, nftRevealType="Day", start=None, end=None):
        uri = '/'.join(['/v3/hedgies/history'])
        return self._get(uri,{'nftRevealType': nftRevealType,'start': start, 'end': end},).data 



#######################
## Public api client ##
#######################
client = Public(host="https://api.dydx.exchange")


#################
## Get Markets ##
#################
## Get all markets
market = pd.DataFrame(client.get_market()['markets'])



####################
## Get Order Book ##
####################
## Returns the active orderbook for a market. All bids and asks that are fillable are returned.
bid = pd.DataFrame(client.get_orderbook('BTC-USD')['bids'])
ask = pd.DataFrame(client.get_orderbook('BTC-USD')['asks'])


################
## Get Trades ##
################

## Get trades from a market
trade = client.get_trade('BTC-USD')
trade = pd.DataFrame(trade['trades'])

## Get trades from a market with defined time & limit
s_trade = client.get_trade('BTC-USD','2021-09-05T17:33:43.163Z','1')
s_trade =  pd.DataFrame(s_trade['trades'])


######################
## Get Market Stats ##
######################
## Get an individual market's statistics over a set period of time or all available periods of time.
## Specified day range for the statistics to have been compiled over. Can be one of 1, 7, 30. Defaults to 1.

stats = client.get_stats("BTC-USD", days=1)
stats = pd.DataFrame(stats['markets'])


############################
## Get Historical Funding ##
############################
## Get the historical funding rates for a market.

funding = client.get_historical_funding("BTC-USD")
funding = pd.DataFrame(funding['historicalFunding'])


#######################
## Get Configuration ##
#######################
## Get any global configuration variables for the exchange as a whole.

config = pd.DataFrame(client.get_config())


#####################
## Get Leaderboard ##
#####################
## Get the top PNLs for a specified period and how they rank against each other.
leader = client.get_leaderboard(period="DAILY", startingBeforeOrAt=None, sortBy='PERCENT', limit='10')
leader = pd.DataFrame(leader['topPnls'])


#################
## Get Hedgies ##
#################
## Get the currently revealed Hedgies for competition distribution.
hedgies = client.get_current_hedgies()
h_daily = pd.DataFrame(hedgies['daily'])
h_weekly = pd.DataFrame(hedgies['weekly'])


## Get the historically revealed Hedgies from competition distributions.
hist_hedgies_d = client.get_hist_hedgies(nftRevealType="daily")
hh_daily = pd.DataFrame(hist_hedgies_d['historicalTokenIds'])

hist_hedgies_w = client.get_hist_hedgies(nftRevealType="weekly")
hh_weekly = pd.DataFrame(hist_hedgies_w['historicalTokenIds'])


#################
## Output data ##
#################
with pd.ExcelWriter('dydx_data.xlsx') as writer:  
    market.to_excel(writer, sheet_name='market') 
    bid.to_excel(writer, sheet_name='bid')
    ask.to_excel(writer, sheet_name='ask')
    trade.to_excel(writer, sheet_name='trade')
    s_trade.to_excel(writer, sheet_name='single_trade')
    stats.to_excel(writer, sheet_name='market_stats')
    funding.to_excel(writer, sheet_name='funding_rate')
    config.to_excel(writer, sheet_name='config')    
    leader.to_excel(writer, sheet_name='leaderboard')
    h_daily.to_excel(writer, sheet_name='hedgies_daily')
    h_weekly.to_excel(writer, sheet_name='hedgies_weekly')
    hh_daily.to_excel(writer, sheet_name='hedgies_daily_hist')
    hh_weekly.to_excel(writer, sheet_name='hedgies_weekly_hist')
