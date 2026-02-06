import yfinance as yf
import pandas as pd

class Trader:
    def __init__(self, stock, from_date, to_date, start_money = 5000):
        self.stock = stock
        self.from_date = from_date
        self.to_date = to_date
        self.start_money = start_money
        
        self.price_table = None
        self.trade_list = []
        
    def download_prices(self):
        table = yf.download(self.stock, start = self.from_date, end = self.to_date, progress = False)
        if isinstance(table.columns, pd.MultiIndex):
            table.columns = table.columns.get_level_values(0)

        #Removing duplicate values and filling the missing values
        table = table[~table.index.duplicated(keep='first')]
        table = table.ffill()
    
        self.price_table = table
        return table
    
    def add_averages(self):
        if self.price_table is None:
            raise ValueError("Run download_prices() first")
        
        self.price_table['MA50'] = self.price_table['Close'].rolling(50).mean()
        self.price_table['MA200'] = self.price_table['Close'].rolling(200).mean()
        
        return self.price_table
    
    def add_signals(self):
        if self.price_table is None:
            raise ValueError("Run download_prices() first")
        
        if 'MA50' not in self.price_table.columns or 'MA200' not in self.price_table.columns:
            raise ValueError("Run download_prices() first")
        
        self.price_table['buy_signal'] = (
            (self.price_table['MA50'] > self.price_table['MA200']) &
            (self.price_table['MA50'].shift(1) <= self.price_table['MA200'].shift(1))
        )
        
        self.price_table['sell_signal'] = (
            (self.price_table['MA50'] < self.price_table['MA200']) &
            (self.price_table['MA50'].shift(1) >= self.price_table['MA200'].shift(1))
        )
        
    def run_trades(self):
        if self.price_table is None:
            raise ValueError("Run download_prices() first")
        
        if 'buy_signal' not in self.price_table.columns:
            raise ValueError("Run add_signals() first")
        table = self.price_table.dropna(subset = ['MA50', 'MA200']).copy()
        
        money = self.start_money
        shares = 0
    
        for day, row in table.iterrows():
            price = float(row['Close'])
            
            if row['buy_signal'] and shares == 0:
                qnty = int(money // price)
                if qnty > 0:
                    shares = qnty
                    money = money - (qnty * price)
                    self.trade_list.append({'date': str(day.date()), 'action': 'BUY', 'price': price, 'qnty': qnty})
                    
            if row['sell_signal'] and shares > 0:
                money = money + (shares * price)
                self.trade_list.append({'date': str(day.date()), 'action': 'SELL', 'price': price, 'qnty': shares})
                shares = 0
            
        if shares > 0:
            last_day = table.index[-1]
            last_price = float(table.iloc[-1]['Close'])
                
            money = money + (shares * last_price)
            self.trade_list.append({'date': str(last_day.date()), 'action': 'SELL_FORCE', 'price': last_price, 'qnty': shares})
                
        profit = money - self.start_money
        return money, profit