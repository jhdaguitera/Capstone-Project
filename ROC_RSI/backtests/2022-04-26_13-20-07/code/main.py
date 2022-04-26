
from AlgorithmImports import *
from QuantConnect.Indicators import *
from yahoo_reader import YahooData
from yahoo_loader import *







class ROC_RSI(QCAlgorithm):    

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
        
        #define open and close prices
        self.open_price = round((data[self.symbol].Open), 2)      
        self.close_price = round((data[self.symbol].Close), 2)
        self.Debug(f"{self.symbol.Value} - {self.Time}: Close={self.close_price}, RSI = {self.rsi}")
        
        #if RSI is less than 30, then BUY
        if self.rsi.Current.Value < 30 and self.Portfolio[self.symbol].Invested <= 0:
            self.Debug("*RSI is less then 30")
            self.SetHoldings(self.symbol, 1) # Allocate % of buying power to stock 
            self.Debug("***Order was placed to BUY***")
        
        #if RSI is more than 70, then SELL
        if self.rsi.Current.Value > 70:
            self.Debug("*RSI is greater then 70")
            self.Liquidate()
            self.Debug("***Order placed to SELL***")           
         
                  
        #Rate of change calculated
        self.roc_since_open = round(((self.close_price - self.open_price) / self.open_price), 2)        
        self.myROC = round((self.roc_since_open * 100), 2)  
        
               
        #if ROC less than 0, then print Down Trend
        if self.roc_since_open < 0:
           self.Debug("Seeing DOWN Trend")
        
        #if ROC is greater than 0, then print Up Trend
        if self.roc_since_open > 0:
           self.Debug("Seeing UP Trend")    
        
        self.Debug("________________________________________________________________________ ")       
    
  
            
            
    #def OnEndOfDay(self):
     #   self.Plot("Indicator","RSI", self.rsi.Current.Value)
        
         
                        
