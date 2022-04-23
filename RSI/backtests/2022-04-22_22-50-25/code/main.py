
from AlgorithmImports import *
from QuantConnect.Indicators import *
from yahoo_reader import YahooData
from yahoo_loader import *


class Relative_Strength_Index(QCAlgorithm):    

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  
        self.SetEndDate(2022, 1, 1)          
        self.SetCash(100000)
        
        self.SetWarmUp(100)                  
        self.ticker = "TQQQ"
        
        get_yahoo_data(self.ticker, '2021-01-01', '2022-01-01')        
        self.symbol = self.AddData(YahooData, self.ticker, Resolution.Daily).Symbol
        
        #calling Relative Strength insdex method and passing in period
        self.rsi = self.RSI(self.symbol, 10)        
        self.Debug("Initilize Complete.")

    def OnData(self, data):        
        if not self.rsi.IsReady: 
            return
    
        #if RSI is less than 30
        if self.rsi.Current.Value < 30 and self.Portfolio[self.symbol].Invested <= 0:
            self.Debug("RSI is less then 30")
            self.SetHoldings(self.symbol,0.5) # Allocate 50% of buying power to stock via market orders.
            self.Debug("Order was placed to BUY")
        
        #if RSI is more than 70
        if self.rsi.Current.Value > 70:
            self.Debug("RSI is greater then 70")
            self.Liquidate()
            self.Debug("Order placed to SELL")
            
    def OnEndOfDay(self):
        self.Plot("Indicators","RSI", self.rsi.Current.Value)
        
                
        
      