# -*- coding: UTF-8 -*-
import csv
import universal
import okex

def get_key_pair(discription="test"):
    f=open('API_list.csv','r')
    reader=csv.reader(f)
    result=[]
    for row in reader:
        if row[9]==discription:
            result= [row[7],row[8],row[3]]
    f.close()
    return result

class Account:
    def __init__(self, description="test"):
        key_pair=get_key_pair(description)
        self.api_key=key_pair[0]
        self.secret_key=key_pair[1]
        self.description=description
        self.name=key_pair[2]

    def set_balance(self, balance_info=None):
        if balance_info.__class__!=universal.BalanceInfo:
            okex1=okex.OKEx(self)
            balance_info=okex1.balances()
        self.balance_info=balance_info  # universal.BalanceInfo class

    def set_orders(self, orders):
        self.orders=orders

    def get_rough_equivalent_asset(self, reference= 'usdt'):
        self.set_balance()
        free=self.balance_info.free
        frozen=self.balance_info.frozen
        total_asset={}
        equivalent_asset=0
        for coin in free:
            total_asset[coin]=float(free[coin])
        for coin in frozen:
            total_asset[coin]+=float(frozen[coin])
        try:
            for coin in total_asset:
                okex1=okex.OKEx(self)
                if total_asset[coin]!=0:
                    if coin==reference:
                        ratio=1
                    else:
                        ratio=(okex1.ticker(coin + '_' + reference)).last
                        if ratio==0:
                            ratio=(okex1.ticker(reference + '_' + coin)).last
                    equivalent_asset+=total_asset[coin]*ratio
        except:
            pass
        return equivalent_asset