# coding=utf-8

import mysql_API
import okex
import account
import json
import universal
import time


def build_batch_data(param):
    # "[{price:10001.1,amount:0.01,type:'sell'},"
    # "{price:10002.2,amount:0.01,type:'sell'}]"
    # data=json.dumps(param, sort_keys=True)
    link=","
    seq=[]
    for item in param:
        seq.append("{price:" + str(item["price"]) + ",amount:" + str(item["amount"]) + ",type:'" + item["type"] + "'}")
    data="[" + link.join(seq) +"]"

    return data

def cancel_previous_orders():
    result=okex1.order_list(currency_pair)
    for order in result.orders:
        if order.status==0 or order.status==1:
            okex1.cancel_order(currency_pair,order.id)

def cancel_all_orders(account, orders):
    # inquire my account occasionally, if there are any pending orders, cancel all
    import time
    global currency_pair
    if int(time.time()) % 60 == 0:
        cancel_previous_orders()
    # cancel the orders, that are created last time
    if len(orders)>0:
        for order in orders:
            okex1.cancel_order(currency_pair,order.id)


def summit_orders(account,prices):
    # clarify the account situation, and reallocate money to different usage:
    global my_info
    my_info=okex1.balances()
    free_btc=float(my_info.free["btc"])
    free_bch=float(my_info.free["bch"])
    frozen_btc=float(my_info.frozen["btc"])
    frozen_bch=float(my_info.frozen["bch"])
    my_bid=prices[0]
    my_ask=prices[1]

    # use free btc to buy bch
    bid_amount=free_btc/my_bid-0.001
    # use free bch to sell for btc
    ask_amount=free_bch-0.001

    # param=[]
    # if bid_amount>0.001:
    #     o=okex1.submit_order(currency_pair=currency_pair,type="buy",price=my_bid,amount=bid_amount)
    #     if o.message=="操作成功":
    #         orders.append(o)
    # if ask_amount>0.001:
    #     p=okex1.submit_order(currency_pair=currency_pair,type="sell",price=my_ask,amount=ask_amount)
    #     if p.message=="操作成功":
    #         orders.append(p)

def if_price_changed():
    pass


currency_pair='bch_btc'
previous_bid=0
previous_ask=999

account=account.Account("test")
okex1=okex.OKEx(account)
my_info=okex1.balances()
ask_order=None
bid_order=None
account.set_balance(my_info)

cancel_previous_orders()
while True:
    depth=okex1.depth(currency_pair)
    ask0=depth.asks[0].price
    bid0=depth.bids[0].price
    my_ask,my_bid=depth.get_supporting_points('vol',1)




    # determine the balance:
    my_info=okex1.balances()
    free_btc=float(my_info.free["btc"])
    free_bch=float(my_info.free["bch"])
    frozen_btc=float(my_info.frozen["btc"])
    frozen_bch=float(my_info.frozen["bch"])

    # use free btc to buy bch
    bid_amount=free_btc/my_bid-0.001
    # use free bch to sell for btc
    ask_amount=free_bch-0.001

    if previous_ask==my_ask:
        print("the ask price stays no change, skip the round")
    else:
        # cancel pending orders
        if ask_order!=None:
            okex1.cancel_order(currency_pair,ask_order.order_id)
        # submit new orders
        if ask_amount>=0.001:
            ask_order = okex1.submit_order(currency_pair=currency_pair,type="sell",price=my_ask,amount=ask_amount)
            previous_ask=my_ask
            print("sell:\tprice: %f\tamount: %f" % ( ask_order.price, ask_order.amount))
    if previous_bid==my_bid:
        print("the bid price stays no change, skip the round")
    else:
        # cancel pending orders
        if bid_order!=None:
            okex1.cancel_order(currency_pair,bid_order.order_id)
        # submit new orders
        if bid_amount>=0.001:
            bid_order = okex1.submit_order(currency_pair=currency_pair,type="buy",price=my_bid,amount=bid_amount)
            previous_bid=my_bid
            print("buy:\tprice: %f\tamount: %f" % ( bid_order.price, bid_order.amount))
    time.sleep(2)
