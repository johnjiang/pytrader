from datetime import datetime
import numpy as np
from pandas.core.series import Series
from models import BollingerStrategy, StrategyEngine


class BollingerStrategyTest(object):
    def __init__(self):
        self.dates = []
        self.prices = []

    def add_price(self, date, price):
        self.dates.append(datetime.strptime(date, "%d/%m/%y"))
        self.prices.append(float(price))

    def run_strategy(self, n, k):
        n = int(n)
        k = float(k)

        prices = Series(self.prices, index=self.dates)

        self.strategy = BollingerStrategy(n=n, k=k)

        self.engine = StrategyEngine([self.strategy], prices)
        self.engine.start()

    def to_list(self, series):
        #Doing this because ubuntu 12.04 comes with numpy 1.6 and so does not have to_list()
        #Also, concordion cannot seem to process nan so we use "" for the time being
        means = []
        for num in series:
            if np.isnan(num):
                means.append("")
            else:
                means.append(round(float(num), 12)) #we round to 12 because that's what excel displays
        return means

    def get_moving_means(self):
        return self.to_list(self.strategy.moving_means)

    def get_upper_bands(self):
        return self.to_list(self.strategy.upper_bands)

    def get_lower_bands(self):
        return self.to_list(self.strategy.lower_bands)

    def get_transactions(self):
        transactions = self.strategy.transactions
        for t in transactions:
            t.date = t.date.strftime("%d/%m/%y")
            t.price = float(t.price)
        return transactions
