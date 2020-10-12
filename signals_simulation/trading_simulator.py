"""
Trading-Technical-Indicators (tti) python library

File name: trading_simulator.py
    Class implementation of a Trading Simulator.
"""

import matplotlib.pyplot as plt


class TradingSimulator:
    """
    Trading Simulator class implementation.

    Parameters:
        indicator_name (str): Indicator name used for this simulation. It is
            used as a part of the title in the produced graph.

    Attributes:
        -

    Raises:
        -
    """

    def __init__(self, indicator_name):

        self._indicator_name = indicator_name

        # Transaction statistics
        self._transaction_stats = {
            'executed_buy_orders': 0, 'executed_sell_orders': 0,
            'ignored_buy_orders': 0, 'ignored_sell_orders': 0}

        # Portfolio details
        self._portfolio = {'stocks': 0, 'balance': 0.0, 'total_value': 0.0}

        # Historical data
        self._history = {'balance': [0.0], 'stocks': [0], 'total_value': [0.0]}

    def buyStocks(self, price, quantity=1, commission=0.0):
        """
        Execute a buy order.

        Parameters:
            price (float): The price of a single stock item.

            quantity (int, default is 1): The number of stocks to be bought.

            commission (float, default is 0.0): The commission for this
                transaction.

        Raises:
            -

        Returns:
            -
        """

        self._portfolio['stocks'] += quantity
        self._portfolio['balance'] -= quantity * price + commission
        self._portfolio['total_value'] = \
            self._portfolio['stocks'] * price + self._portfolio['balance']

        self._history['balance'].append(self._portfolio['balance'])
        self._history['stocks'].append(self._portfolio['stocks'])
        self._history['total_value'].append(self._portfolio['total_value'])

        self._transaction_stats['executed_buy_orders'] += 1

    def sellStocks(self, price, quantity=int(1e+06), commission=0.0):
        """
        Execute a sell order.

        Parameters:
            price (float): The price of a single stock item.

            quantity (int, default is 1e+06): The number of stocks to be sold.

            commission (float, default is 0.0): The commission for this
                transaction.

        Raises:
            -

        Returns:
            -
        """

        if self._portfolio['stocks'] == 0:
            self._transaction_stats['ignored_sell_orders'] += 1

        else:
            self._portfolio['balance'] += \
                min(quantity, self._portfolio['stocks']) * price - commission
            self._portfolio['stocks'] = 0
            self._portfolio['total_value'] = self._portfolio['balance']

            self._history['balance'].append(self._portfolio['balance'])
            self._history['stocks'].append(self._portfolio['stocks'])
            self._history['total_value'].append(self._portfolio['total_value'])

            self._transaction_stats['executed_sell_orders'] += 1

    def _updateTotalValue(self, price):
        """
        Updates the total value of the portfolio. Total-Value = Balance +
        Stocks-Value.

        Parameters:
            price (float): The price of a single stock item.

        Raises:
            -

        Returns:
            -
        """
        self._portfolio['total_value'] = \
            self._portfolio['stocks'] * price + self._portfolio['balance']
        self._history['total_value'][-1] = self._portfolio['total_value']

    def getPortfolioInfo(self, price):
        """
        Returns information about Portfolio.

        Parameters:
            price (float): The latest price of a single stock item. Is used
                for calculating the Total-Value before returning the requested
                information.

        Raises:
            -

        Returns:
            (dict): The portfolio information.
        """

        self._updateTotalValue(price=price)

        return self._portfolio

    def getTransactionsInfo(self):
        """
        Returns information about Transactions.

        Parameters:
            -

        Raises:
            -

        Returns:
            (dict): The transactions information.
        """

        return self._transaction_stats

    def getHistoryGraph(self):
        """
        Returns a matplotlib.pyplot graph with historical data about balance,
        stocks and total value.

        Parameters:
            -

        Raises:
            -

        Returns:
            (matplotlib.pyplot): The produced graph.
        """

        plt.figure(figsize=(7, 5))

        plt.subplot(3, 1, 1)
        plt.plot(list(range(1, len(self._history['balance'])+1)),
                 self._history['balance'], label='balance', color='limegreen')
        plt.legend(loc=0)
        plt.grid(which='major', axis='y', alpha=0.5)
        plt.title('Trading Simulation - ' + self._indicator_name, fontsize=11,
                  fontweight='bold')
        plt.gca().axes.get_xaxis().set_visible(False)

        plt.subplot(3, 1, 2)
        plt.plot(list(range(1, len(self._history['stocks']) + 1)),
                 self._history['stocks'], label='stocks', color='tomato')
        plt.legend(loc=0)
        plt.grid(which='major', axis='y', alpha=0.5)
        plt.gca().axes.get_xaxis().set_visible(False)

        plt.subplot(3, 1, 3)
        plt.plot(list(range(1, len(self._history['total_value']) + 1)),
                 self._history['total_value'], label='total_value',
                 color='cornflowerblue')
        plt.legend(loc=0)
        plt.grid(which='major', axis='y', alpha=0.5)
        plt.xlabel('Transactions', fontsize=11, fontweight='bold')
        plt.gcf().text(0.04, 0.5, 'Total Value | Stocks | Balance',
                       fontsize=11, fontweight='bold', va='center',
                       rotation='vertical')

        return plt
