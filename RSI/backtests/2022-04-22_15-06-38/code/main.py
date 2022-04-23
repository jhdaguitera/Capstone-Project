class EmotionalFluorescentOrangeAntelope(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2021, 3, 1)
        self.SetEndDate(2021, 3, 3)
        self.SetCash(100000) 
        self.symbol = self.AddEquity("SPY", Resolution.Minute).Symbol
        
        self.open_price = None
        self.day = 0


    def OnData(self, data):
        if not (data.ContainsKey(self.symbol) and data[self.symbol] is not None):
            return
        
        if data.Time.day != self.day:
            self.open_price = data[self.symbol].Open
        self.day = data.Time.day
        
        close_price = data[self.symbol].Close
        roc_since_open = (close_price - self.open_price) / self.open_price
        self.Plot("ROC", "Since Open", roc_since_open)