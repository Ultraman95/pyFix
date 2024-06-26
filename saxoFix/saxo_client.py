# -*- coding: utf-8 -*-
"""
    QuickFIX_Test_Client.py
    
    A user defined class that must include 
    on_tick() and on_execution_report() methods.


FIX tags:
https://www.onixs.biz/fix-dictionary/4.4/fields_by_tag.html

tags for all message types:
https://www.fixtrading.org/online-specification/trade-appendix/


"""

from time import sleep

from appfix.client import client
from appfix.order import order


class tick_processor():

    def __init__(self):

        # to handle QuickFIX own message logging, change in config file:
        # ScreenLogShowIncoming=Y
        # ScreenLogShowOutgoing=Y
        # ScreenLogShowEvents=Y
        print('Starting Saxo_client...')
        self.client = client(self, config_file='config/client.cfg', 
                             read_positions_from_file=False,     # to load positions after restart
                             store_all_ticks=True,               # to store all incoming ticks
                             save_history_to_files=True,         # to save the price history to file
                             verbose=False,                       # to control the print output
                             message_log_file = 'messages.log',  # if the file names are set to an empty string, the specific logger will be disabled. 
                             execution_history_file='execution_history.log')

        self.trade_done = False
        self.cancel_done = False

    """
    # override this method with your own logic. 
    # it is executed on every price update. 
    """
    def on_tick(self, symbol, app):

        # # Symbol is the one that got a price or execution update.
        # print('Price update for', symbol, '| bid:', app.history_dict[symbol].BID_TOB, '| ask:', app.history_dict[symbol].ASK_TOB)

        # access current bid/ask prices and order book sizes. 
        # print('prices:', app.history_dict[symbol].BID, app.history_dict[symbol].ASK, 
        #       ' | sizes:', app.history_dict[symbol].BID_SIZE, app.history_dict[symbol].ASK_SIZE)
        
        # access tick history (use HISTORY_TOB for top-of-book history):
        # print('Symbol ticks received:', len(app.history_dict[symbol].HISTORY))

        # to generate candle data for a specific time frame:
        # print(app.history_dict[symbol].resampled_history('bid', '5min'))

        # # open order can also be accessed through a dictionary app.open_orders. 
        print(symbol, 'open orders:', app.num_orders(symbol))

        # net positions can be accessed through a dictionary app.open_net_positions. 
        print(symbol, 'NET POSITION | filled:', app.net_position(symbol), '| canceled:', app.canceled_net_quantity[symbol])

        # to enter a trade:
        # if not self.trade_done:
        #     self.trade_done = True

        #     # app.sender.send_OrderCancelRequest(1)

        #     # price = app.history_dict[symbol].ASK_TOB  # app.history_dict[symbol].ASK_TOB  # top of book ASK price

        #     # possible order_types: 'buy_market', 'buy_limit', 'buy_stop', 'sell_market', 'sell_limit', 'sell_stop'
        #     # if ClOrdID is not given, it will use an internal counter. 
        #     # price must only be given for limit or stop orders. 
        #     _order = order(order_type='buy_market', symbol=symbol, 
        #                    quantity=1000)  # , ttl=30000
        #     print('#----------------------------------------------------------------------#')
        #     print('isLoggedOn:', self.client.isLoggedOn())
        #     print('Sending order:')
        #     print(_order)

            # # to send the order:
            # app.sender.send_NewOrderSingle(_order)


    """
    # override this method with your own logic. 
    # it is executed on receiving a new execution report. 
    """
    def on_execution_report(self, report, app):
        # you can also access all historic execution reports through the list app.execution_history. 
        print('\nExecution Report:')
        print(report)

        print('Open orders:')
        for key in app.open_orders.keys():
            print(key, '|', app.open_orders[key])
        

##############################################################################

if __name__=='__main__':
    processor = tick_processor()

    while processor.client.isLoggedOnQuote():
        # demo:
        symbols = ['EUR/USD']

        # live:
        # symbols = ['EURUSD', 'GBPUSD', 'USDJPY']

        for symbol in symbols:
            print("send_MarketDataRequest symbol=", symbol)
            processor.client.subInstrument(symbol)
            sleep(1)
        break

    sleep(5)

    '''
    while processor.client.isLoggedOnTrade():
        _order = order(order_type='buy_market', symbol='EUR/USD', quantity=100)
        processor.client.orderInsert(_order)
        break

    # keep the thread alive.
    #while processor.client.isLoggedOn():
    #    sleep(60)
    '''

    input('Press Enter to exit...')
        
    ##processor.client.stop()
