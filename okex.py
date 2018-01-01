# it's highly suggested to use ENGLISH only in this project

import account
import universal

from HttpMD5Util import buildMySign,httpGet,httpPost

class OKEx:

    __market="OKEx"

    def __init__(self,account, base_url = 'www.okex.com'):
        "account represents a key pair, base_url represents the prefix of the restFUL resources"
        self.account=account
        self.base_url=base_url

    # 获取OKCOIN现货行情信息
    def ticker(self, currency_pair='btc_usdt'):
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params = ''
        if currency_pair:
            params = 'symbol=%(symbol)s' % {'symbol': currency_pair}
        result=universal.Ticker(self.__market,currency_pair, httpGet(self.base_url, TICKER_RESOURCE, params))
        return result

    # 获取OKCOIN现货市场深度信息
    def depth(self, currency_pair='btc_usdt', raw=True):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params = ''
        if currency_pair:
            params = 'symbol=%(symbol)s' % {'symbol': currency_pair}
        result=httpGet(self.base_url, DEPTH_RESOURCE, params)
        if raw==False:
            return result
        else:
            result=universal.Depth(self.__market,currency_pair,result)
            return result

    # 获取OKCOIN现货历史交易信息
    def trades(self, currency_pair=''):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params = ''
        if currency_pair:
            params = 'symbol=%(symbol)s' % {'symbol': currency_pair}
        return httpGet(self.base_url, TRADES_RESOURCE, params)

    # 获取用户现货账户信息
    def balances(self):
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params = {}
        params['api_key'] = self.account.api_key
        params['sign'] = buildMySign(params, self.account.secret_key)
        result=httpPost(self.base_url, USERINFO_RESOURCE, params)
        result=universal.BalanceInfo(self.__market,result)
        return result

    # 现货交易
    def submit_order(self, type="buy", currency_pair='btc_usdt',  price='', amount=''):
        if type==1 or type=="1" or type.lower()=="buy":
            type="buy"
        else:
            type="sell"
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': self.account.api_key,
            'symbol': currency_pair,
            'type': type
        }
        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount

        params['sign'] = buildMySign(params, self.account.secret_key)
        return httpPost(self.base_url, TRADE_RESOURCE, params)

    #现货取消订单
    def cancel_order(self,currency_pair,order_id):
        CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
        params = {
            'api_key':self.account.api_key,
            'symbol':currency_pair,
            'order_id':order_id
        }
        params['sign'] = buildMySign(params,self.account.secret_key)
        return httpPost(self.base_url,CANCEL_ORDER_RESOURCE,params)

    #现货订单信息查询, 此方法为独享方法
    def orderinfo(self,symbol,orderId):
        ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
        params = {
            'api_key':self.__apikey,
            'symbol':symbol,
            'order_id':orderId
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,ORDER_INFO_RESOURCE,params)

    # order_list这个方法是取得未成交订单的列表！
    def order_list(self,currency_pair, current_page=1, page_length=200):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': self.account.api_key,
            'symbol': currency_pair,
            'status': 0,
            'current_page': current_page,
            'page_length': page_length
        }
        params['sign'] = buildMySign(params, self.account.secret_key)
        return httpPost(self.base_url, ORDER_HISTORY_RESOURCE, params)

    # trade_list这个方法是取得已成交订单的列表！
    def trade_list(self,currency_pair, current_page=1, page_length=200):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': self.account.api_key,
            'symbol': currency_pair,
            'status': 1,
            'current_page': current_page,
            'page_length': page_length
        }
        params['sign'] = buildMySign(params, self.account.secret_key)
        return httpPost(self.base_url, ORDER_HISTORY_RESOURCE, params)

    #现货批量下单
    def batch_trade(self,currency_pair,type,orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key':self.account.api_key,
            'symbol':currency_pair,
            'type':type,
            'orders_data':orders_data
        }
        params['sign'] = buildMySign(params,self.account.secret_key)
        return httpPost(self.base_url,BATCH_TRADE_RESOURCE,params)

    def trade_history(self, currency_pair, since):
        TRADE_HISTORY_RESOURCE="/api/v1/trade_history.do"
        params={
            'api_key': self.account.api_key,
            'symbol': currency_pair,
            'since': since,
        }
        params['sign'] = buildMySign(params,self.account.secret_key)
        return httpPost(self.base_url, TRADE_HISTORY_RESOURCE, params)

    def get_all_currencies(self):
        import json
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params = {}
        params['api_key'] = self.account.api_key
        params['sign'] = buildMySign(params, self.account.secret_key)
        result=json.loads(httpPost(self.base_url, USERINFO_RESOURCE, params))
        result=result["info"]["funds"]["free"]
        result=dict(result).keys()
        currencies=[]
        for item in result:
            currencies.append(item)
        return currencies

    def get_all_currency_pairs(self):
        import currency_pair
        currencies=self.get_all_currencies()
        references=currency_pair.CurrencyPair().get_referencial_currencies("okex")
        currency_pairs=[]
        for reference in references:
            for currency in currencies:
                if str(currency).lower()!=str(reference).lower():
                    currency_pairs.append(str(currency)+"_"+str(reference))
        return currency_pairs


    def get_currency_pair_order(self, top_n=10, ordered_by="trading volume"):
        '''
        this method returns a list of currency pairs ordered by trading volume
        :param top_n: how many currency pairs you want to list
        :param ordered_by: either of 'trading volume', 'market cap', 'price', etc.
        :return: a list of currency pairs ordered by trading volume
        '''
        # get all the currency pairs:
        import currency_pair as cp
        all_currency_pairs=self.get_all_currency_pairs()


        # get the ratio of ref1 to usdt
        cp1=cp.CurrencyPair()
        referencial_currencies=cp1.get_referencial_currencies("okex")
        prices_of_referencial_currencies={}
        for currency in referencial_currencies:
            if currency!="usdt":
                ticker=self.ticker(currency+"_usdt")
                price=ticker.last
                prices_of_referencial_currencies[ticker.currency_pair]=price


        tickers=[]
        turn_volumes={}

        for currency_pair in all_currency_pairs:
            referencial_currency=cp1.get_referencial_currency(str(currency_pair))
            if referencial_currency!="usdt":
                ticker=self.ticker(currency_pair)
                if ticker.message=="True":
                    turn_volume=(ticker.high+ticker.low)*ticker.vol*prices_of_referencial_currencies[referencial_currency+"_usdt"]/2
                    turn_volumes[ticker.currency_pair]=turn_volume
        turn_volumes=sorted(turn_volumes.items(), key=lambda x:x[1], reverse=True)
        return turn_volumes[:top_n-1]





