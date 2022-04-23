
from AlgorithmImports import *
from yahoo_reader import YahooData
from yahoo_loader import *

#import numpy as np


class ROC(QCAlgorithm):    

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  
        self.SetEndDate(2022, 1, 1)    
        self.SetCash(100000)         
        self.ticker = "TQQQ"
        
        get_yahoo_data(self.ticker, '2021-01-01', '2022-01-01')
        
        
        # self.AddEquity("SPY", Resolution.Minute)      
        self.symbol = self.AddData(YahooData, self.ticker, Resolution.Daily).Symbol
        
        # request the forex data
        #self.AddForex("EURGBP", Resolution.Hour, Market.Oanda)
       # self.SetBrokerageModel(BrokerageName.OandaBrokerage) 
        self.rsi = self.RSI(self.ticker, 14)
        
        self.Debug("Initilize is complete")

    def OnData(self, data):
        
        if not self.rsi.IsReady: 
            return
    
        if self.rsi.Current.Value < 30 and self.Portfolio[self.ticker].Invested <= 0:
            self.Debug("RSI is less then 30")
            self.MarketOrder(self.ticker, 2500)
            self.Debug("Market order was placed to BUY")
        
        if self.rsi.Current.Value > 70:
            self.Debug("RSI is greater then 70")
            self.Liquidate()
            self.Debug("Market order was closed to SELL")
            
    def OnEndOfDay(self):
        self.Plot("Indicators","RSI", self.rsi.Current.Value)
        
                
        
        #if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1)