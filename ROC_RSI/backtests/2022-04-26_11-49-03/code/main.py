
from AlgorithmImports import *
from QuantConnect.Indicators import *
from yahoo_reader import YahooData
from yahoo_loader import *


class ROC_in_Percent(QCAlgorithm): 

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  
        self.SetEndDate(2022, 1, 1)          
        self.SetCash(100000)
        
        self.SetWarmUp(100)                  
        self.ticker = "TQQQ"
        
        get_yahoo_data(self.ticker, '2021-01-01', '2022-01-01')        
        self.symbol = self.AddData(YahooData, self.ticker, Resolution.Daily).Symbol        
                                  
        self.Debug("Initilize Complete.")

    def OnData(self, data):                        
        if not (data.ContainsKey(self.symbol) and data[self.symbol] is not None):
                return
 
       #define open and close prices
        self.open_price = round((data[self.symbol].Open), 2)      
        self.close_price = round((data[self.symbol].Close), 2)
        
       #Momentum calculated
        self.mom = round(((self.close_price - self.open_price) * 100, 0)            
       
        #Rate of change calculated
        self.roc_since_open = round(((self.close_price - self.open_price) / self.open_price), 2)        
        self.ROC_Percent = round((100 * self.roc_since_open), 2)      
        
        #print out
        self.Debug(f"{self.symbol.Value} - {self.Time}: Close={self.close_price}")
        self.Debug(f"Momentum = {self.mom})
        self.Debug(f"ROC Percent = {self.ROC_Percent}%")
       
       ## This is logic still needs work...do not trade based soley on ROC (seeing whipsaw)      
        
         #if ROC less than 0, then Down Trend
        if self.roc_since_open < 0:
           self.Debug("DOWN Trend**********************************************")
           # self.Debug("ROC less than 0")
          #  self.Liquidate()           
           # self.Debug("Order was placed to SELL")
        
        #if ROC is greater than 0, then Up Trend
        if self.roc_since_open > 0:
           self.Debug("UP Trend*************************************************")
           # self.Debug("ROC is greater then 0")
           # self.SetHoldings(self.symbol, 1) # Allocate % of buying power to stock 
           # self.Debug("Order placed to BUY")
                        
       