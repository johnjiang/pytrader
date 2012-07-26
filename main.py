#!/usr/bin/env python
"""
    PyTrader is written as part of the Python Coding Assignment for Tibra.

    General Usage:
        $ ./main -h

    Custom Usage:
        To run PyTrader against a set of precompiled prices rather than a ticker. Simply call the
        run_engine function directly, providing a series of prices, n and k.

    Tests
        Tests are stored in under the PyTrader/tests directory. A concordion test covers the
        Bollinger Bands Strategy. In order to execute it, pyconcordion must be installed and it needs
        to be compiled against jdk6. Currently jdk7 is not supported.

    Dependencies:
        All dependencies were installed via Ubuntu's apt-get using default sources from 12.04.

    Notes:
        I use ystockquote as my source for stock prices. I had to modify the get_historical_prices
        slightly so that it can actually work rather than...well...not work.
"""

import argparse
from datetime import datetime
from pandas.core.series import Series

from lib import ystockquote
from models import StrategyEngine, BollingerStrategy


def run_engine(prices, n, k):
    """
        Takes in a series of prices, n-period and k width.
        Specified a predetermiend strategy, runs it and plots graph determined by the strategy.
    """
    strategies = {"Bollinger": BollingerStrategy(n=n, k=k)}
    engine = StrategyEngine(strategies, prices)
    engine.start()
    engine.strategies["Bollinger"].plot()


def main(stock, start_date, end_date, n, k):
    prices = []
    dates = []

    results = ystockquote.get_historical_prices(stock, start_date, end_date)
    for result in reversed(results[1:]): #skipping header, sort in chronological order
        prices.append(float(result[1]))
        dates.append(datetime.strptime(result[0], "%Y-%m-%d"))

    prices_s = Series(prices, index=dates)
    run_engine(prices_s, n, k)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Let's trade")
    parser.add_argument('-n', type=int, default=20, help='N period')
    parser.add_argument('-k', type=float, default=0.75, help='K width')
    parser.add_argument('stock', type=str, nargs=1, help='Stock/Ticker symbol')
    parser.add_argument('start_date', type=str, nargs=1, help='Start Date: YYYYMMDD')
    parser.add_argument('end_date', type=str, nargs=1, help='End Date: YYYYMMDD')

    args = parser.parse_args()
    main(args.stock[0], args.start_date[0], args.end_date[0], args.n, args.k)
