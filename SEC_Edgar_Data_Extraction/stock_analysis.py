import requests
from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np

class stock_analysis(object):
    
    def __init__(self, tickers : str) -> None:
        self.tickers = tickers

    def stock_div(self):
        div = []
        for i in range(0, len(self.tickers)):
            new_row = []
            data = yf.Ticker(str(self.tickers[i]))
            dividend = data.actions
            new_row.insert(0, {"Dividends" : str(self.tickers[i]), "Stock Splits" : None})
            div.append(pd.concat([pd.DataFrame(new_row), dividend], ignore_index=False))
        
        div_compiled = pd.concat(div)
        # insert file path
        div_compiled.to_csv("C:.../dividends.csv", index=True)
        return div_compiled

    def stats_table(self) -> None:
        
        stats = []

        def key_stats(website) -> None:
            r = requests.get(website, headers = {'User-Agent':'Mozilla/5.0'})
            df_list = pd.read_html(r.text)
            result_df = df_list[0]
            for df in df_list[1:]:
                result_df = result_df.append(df)
            return result_df.set_index(0).T

        for i in range(0, len(self.tickers)):
            values = pd.DataFrame(key_stats('https://sg.finance.yahoo.com/quote/'+ str(self.tickers[i]) +'/key-statistics?p='+ str(self.tickers[i])))
            values.insert(0,"Ticker", str(self.tickers[i]))
            stats.append(values)

        result = pd.concat(stats)

        return result

display = stock_analysis(['AAPL', 'AMZN', 'BLK', 'T', 'TSLA'])
print(display.stock_div())


