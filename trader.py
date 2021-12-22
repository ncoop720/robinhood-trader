from dotenv import load_dotenv
from math import ceil, floor
from os import getenv
from pyotp import TOTP
from robin_stocks import *

load_dotenv()
cutoff = 50

def main():
  username = getenv('ROBINHOOD_USERNAME')
  password = getenv('ROBINHOOD_PASSWORD')
  mfa_code = TOTP(getenv('ROBINHOOD_KEY')).now()
  # print(f'Username: {username}, Password: {password}, MFA: {totp}')
  robinhood.login(username, password, mfa_code=mfa_code)

  holdings = robinhood.build_holdings()
  for ticker in holdings:
    equity = float(holdings[ticker]['equity'])
    equity_diff = equity - cutoff
    print(f'{ticker} {equity_diff}')
    if equity_diff >= 1:
      print(f'Selling ${floor(equity_diff)} of {ticker}')
      robinhood.orders.order_sell_fractional_by_price(ticker, floor(equity_diff))
    elif equity_diff <= -1:
      print(f'Buying {ceil(equity_diff)} of {ticker}')
      robinhood.orders.order_buy_fractional_by_price(ticker, ceil(equity_diff))

if __name__ == "__main__":
  main()