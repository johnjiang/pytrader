import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import mean
from numpy.core.numeric import NaN
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from pandas.stats.moments import rolling_mean


class Transaction(object):
    """
        Simple transaction object that holds the number of units, price and date.
    """

    def __init__(self, units, price, date):
        self.units = units
        self.price = price
        self.date = date

    def value(self, transaction_cost_base=0, transaction_cost_perc=0):
        """
            Returns the value of the transaction, can allow for optional transaction fees.
        """
        value = self.units * self.price
        value += math.fabs(value) * transaction_cost_perc
        value += transaction_cost_base
        return value


class StrategyEngine(object):
    """
        Runs a set of strategies given a set of prices. Strategies are supplied as a dictionary.
    """

    def __init__(self, strategies, prices):
        self.prices = prices
        self.transactions = []
        self.strategies = strategies

    def start(self):
        """
            Iterates over the priceses and executes the strategy. Performs a buy/sell depending on
            the trigger generated.
        """
        for date, price in self.prices.iteritems():
            for strategy in self.strategies.values():
                strategy.tick(date, price)


class Strategy(object):
    """
        Abstract object that all strategies should inherit.
    """

    def __init__(self):
        pass

    def tick(self, date, price):
        """
            Every strategy should implement the tick function. This is called everytime a price
            needs to be evaluated by the various Strategies.
        """
        raise NotImplemented

    def plot(self):
        raise NotImplemented


class BollingerStrategy(Strategy):
    def __init__(self, n, k, default_units=10):
        super(BollingerStrategy, self).__init__()
        self.n = n
        self.k = k
        self.default_units = default_units
        self.prices = []
        self.dates = []
        self.upper_bands = []
        self.lower_bands = []
        self.transactions = []

    @property
    def moving_means(self):
        """
            A moving average of all the prices used in the strategy, uses a window as specified by self.n
        """
        return rolling_mean(np.array(self.prices), window=self.n)

    @property
    def last_n_prices(self):
        """
            Returns the last n prices, if n prices are not yet available returns NaN
        """
        last_n_prices = self.prices[-self.n:]
        return last_n_prices if len(last_n_prices) == self.n else NaN

    def _moving_mean(self):
        """
            Returns mean of the last n prices
        """
        return mean(self.last_n_prices)

    def _std(self):
        """
            Returns standard Deviation of the last n prices
        """
        return np.std(self.last_n_prices)

    def _upper_band(self):
        """
            Returns upper bollinger band
        """
        return self._moving_mean() + self.k * self._std()

    def _lower_band(self):
        """
            Returns lower bollinger band
        """
        return self._moving_mean() - self.k * self._std()

    def tick(self, date, price):
        """
            Returns a buy trigger if price is above the upper bollinger band or a
            sell trigger if price is below the lower bollinger band
        """
        self.prices.append(price)
        self.dates.append(date)

        upper_band = self._upper_band()
        lower_band = self._lower_band()

        self.upper_bands.append(upper_band)
        self.lower_bands.append(lower_band)

        if price > upper_band:
            self.transactions.append(Transaction(units=self.default_units, price=price, date=date))
        elif price < lower_band:
            self.transactions.append(Transaction(units=-self.default_units, price=price, date=date))

    def plot(self):
        """
            Plots 2 graphs. One for N-period moving average, lower and upper bands.
            One for P/N and position.
        """

        columns = {"Upper Bands": self.upper_bands,
                   "Lower Bands": self.lower_bands,
                   "Moving Means": self.moving_means,
                   "Opening Prices": self.prices}
        df = DataFrame(columns, index=self.dates)
        df.plot()

        fig = plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
        fig.add_subplot(121)
        trans_dates = [tran.date for tran in self.transactions]
        # we negate the value here to show profit/loss
        trans = Series([-tran.value() for tran in self.transactions], index=trans_dates)
        position = Series([tran.units for tran in self.transactions], index=trans_dates)

        position.cumsum().plot(label="Position")
        plt.xlabel("Date")
        plt.ylabel("Position")
        plt.title("Position over Time")
        plt.legend(loc="best")

        fig.add_subplot(122)
        trans.cumsum().plot(label="P/L")
        plt.xlabel("Date")
        plt.ylabel("Profit/Loss")
        plt.title("Profit and Loss over Time")
        plt.legend(loc="best")

        plt.show()
