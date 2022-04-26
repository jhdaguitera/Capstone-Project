
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
        
        #calling Relative Rate of Change Percent method and passing in period       
        self.ROC_percent = self.ROCP(self.symbol, 10)                     
        self.Debug("Initilize Complete.")

    def OnData(self, data):                    
        if not self.ROC_percent.IsReady: 
            return    
        
        if self.ROC_percent.IsReady:
            if data.ContainsKey(self.symbol):
                if data[self.symbol] is not None:
                    self.Debug("ROC: " + str(self.ROC_percent.Current.Value))