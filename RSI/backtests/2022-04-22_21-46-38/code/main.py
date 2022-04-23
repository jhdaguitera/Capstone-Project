
from AlgorithmImports import *
#from yahoo_reader import YahooData
#from yahoo_loader import *
import numpy as np


class ROC(QCAlgorithm):
    '''Basic template algorithm simply initializes the date range and cash'''

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  #Set Start Date
        self.SetEndDate(2022, 1, 1)    #Set End Date
        self.SetCash(10000)           #Set Strategy Cash
        
        
        #self.AddEquity("SPY", Resolution.Second)
       
        # request the forex data
        self.AddForex("EURGBP", Resolution.Hour, Market.Oanda)
        self.SetBrokerageModel(BrokerageName.OandaBrokerage) 
        self.rsi = self.RSI("EURGBP", 14)
        
        self.Debug("Initilize is complete")

    def OnData(self, data):
        
        if not self.rsi.IsReady: 
            return
    
        if self.rsi.Current.Value < 30 and self.Portfolio["EURGBP"].Invested <= 0:
            self.Debug("RSI is less then 30")
            self.MarketOrder("EURGBP", 25000)
            self.Debug("Market order was placed to buy")
        
        if self.rsi.Current.Value > 70:
            self.Debug("RSI is greater then 70")
            self.Liquidate()
            self.Debug("Market order was closed to sell off")
            
    def OnEndOfDay(self):
        self.Plot("Indicators","RSI", self.rsi.Current.Value)
        
                
        
        #if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1)