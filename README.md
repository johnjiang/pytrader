pytrader
========
Backtesting Framework in Python


General Usage:
==============
    $ ./main -h

Custom Usage:
=============
To run PyTrader against a set of precompiled prices rather than a ticker. Simply call the run_engine function directly, providing a series of prices, n and k.

Tests:
=========
Tests are stored in under the PyTrader/tests directory. A concordion test covers the Bollinger Bands Strategy. In order to execute it, pyconcordion must be installed and it needs to be compiled against jdk6. Currently jdk7 is not supported.

Dependencies:
==============
All dependencies were installed via Ubuntu's apt-get using default sources from 12.04.

Notes:
=========
I use ystockquote as my source for stock prices. I had to modify the get_historical_prices slightly so that it can actually work rather than...well...not work.
