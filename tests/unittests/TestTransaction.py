import unittest

from models import Transaction


class TestTransaction(unittest.TestCase):
    def test_transaction_value_buy(self):
        t = Transaction(units=10, price=5, date=None)

        self.assertEqual(t.value(), 50)

        self.assertEqual(t.value(transaction_cost_base=5), 55)

        self.assertAlmostEqual(t.value(transaction_cost_base=5, transaction_cost_perc=0.10), 60)

        self.assertAlmostEqual(t.value(transaction_cost_perc=0.15), 57.5)

    def test_transaction_value_sell(self):
        t = Transaction(units=-10, price=5, date=None)

        self.assertEqual(t.value(), -50)

        self.assertEqual(t.value(transaction_cost_base=5), -45)

        self.assertAlmostEqual(t.value(transaction_cost_base=5, transaction_cost_perc=0.10), -40)

        self.assertAlmostEqual(t.value(transaction_cost_perc=0.15), -42.5)
