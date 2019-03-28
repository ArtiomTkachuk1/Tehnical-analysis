инкапсулировать(это так называется?) все функции сюда?Или не надо?(можно не)
class product:
    name=""
    prices=pd.DataFrame()
    def loadprices():#загружает df цен позиции
        self.prices=prices_from_alphavantage_response(API_KEY,self.name,"csv")
    def drawprices()#рисует цены
        fig,ax = plt.subplots(figsize=(8, 8))
        ax.plot(self.prices.index, self.prices["close"],color=color, linewidth=1, alpha=0.4)
    def drawcandlestick():#рисует японские свечки цен позиции
        fig, ax = plt.subplots(figsize=(7, 7))
        candlestick2_ohlc(ax,self.prices['open'],self.prices['high'],self.prices['low'],self.prices['close'],width=0.5) 
        ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
        xdate = self.prices.index.date
        def mydate(x,pos):
            try:
                return xdate[int(x)]
            except IndexError:
                return ''
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()
    def getbollinger(window=3,safety=1):#создаёт dataframe для стратегий Боллинжера
        self.prices["close rolling"]=self.prices["close"].rolling(window).mean()
        tmp=safety*self.prices["close"].rolling(window).std()
        self.prices["close top"]=self.prices["close rolling"]+tmp
        self.prices["close bottom"]=self.prices["close rolling"]-tmp
        #first_date=bollingerprices.first_valid_index()
        #first_clean_date=first_date+pd.DateOffset(days=window)
        self.prices=self.prices.iloc[window:]
    def drawbollinger():#рисует график цен, скользящее среднее и линии Боллинжера
        drawcandlestick()
        color='#0066FF'
        fig,ax = plt.subplots(figsize=(8, 8))
        ax.set_title('Price and Bollinger Bands')
        ax.set_xlabel('Date')
        ax.set_ylabel('SMA and Bollinger Bands')
        ax.plot(self.prices.index, self.prices["close rolling"], color=color)
        ax.fill_between(
                self.prices.index,  
                self.prices["close bottom"],
                self.prices["close top"],
                color=color, alpha=0.1)
        ax.plot(
                self.prices.index,  
                self.prices["close bottom"],
                self.prices["close top"],
                color=color, linewidth=1, alpha=0.4)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
        myFmt = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(myFmt)
        fig.autofmt_xdate()