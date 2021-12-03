from dotenv import load_dotenv
from math import floor
from os import getenv
from pyotp import TOTP
from robin_stocks import *

load_dotenv()
cutoff = 50

def main():
  robinhood.login(
    getenv('USERNAME'),
    getenv('PASSWORD'),
    mfa_code=TOTP(getenv('KEY')).now()
  )

  holdings = robinhood.build_holdings()
  for ticker in holdings:
    equity = float(holdings[ticker]['equity'])
    equity_diff = equity - cutoff
    if equity_diff >= 1:
      print(f'Selling ${floor(equity_diff)} of {ticker}')
      robinhood.orders.order_sell_fractional_by_price(ticker, floor(equity_diff))

if __name__ == "__main__":
  main()