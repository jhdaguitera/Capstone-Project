
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
        
        self.open_price = None
        self.day = 0                           
        self.Debug("Initilize Complete.")

    def OnData(self, data):                        
        if not (data.ContainsKey(self.symbol) and data[self.symbol] is not None):
                return
        
        if data.Time.day != self.day:
            self.open_price = data[self.symbol].Open
            
        self.day = data.Time.day
        
        self.close_price = data[self.symbol].Close
        self.roc_since_open = round(((self.close_price - self.open_price) / self.open_price), 3)
        self.ROC_Percent = round((100 * self.roc_since_open), 3)
        self.Debug(f"{self.symbol.Value} - {self.Time}: Close={data[self.symbol].Close}")
        self.Debug(f"ROC = {self.roc_since_open}, ROC Percent = {self.ROC_Percent}%")
                        
        #self.Plot("ROC", "Since Open", roc_since_open)