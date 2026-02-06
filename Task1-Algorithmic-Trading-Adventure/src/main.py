from strategy import Trader

t = Trader("AAPL", "2018-01-01", "2023-12-31")
t.download_prices()
t.add_averages()
t.add_signals()

final_money, profit = t.run_trades()

print("\nFinal money:", final_money)
print("\n\nProfit:", profit)

print("\n\nTotal trades:", len(t.trade_list))
print("\n\n",t.trade_list,"\n")
