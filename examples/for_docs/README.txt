### tti indicators examples

Technical Indicator data:
                      adl
Date
1998-10-05  5.346066e+05
1998-10-06  9.788753e+05
1998-10-07  1.377338e+06
1998-10-08  1.251994e+06
1998-10-09  1.108012e+06
...                  ...
2020-11-30  1.736986e+07
2020-12-01  1.741746e+07
2020-12-02  1.737860e+07
2020-12-03  1.741683e+07
2020-12-04  1.742771e+07

[5651 rows x 1 columns]

Technical Indicator value at 2012-09-06: [8617026.854250321]

Most recent Technical Indicator value: [17427706.42639293]

Technical Indicator signal: ('buy', -1)

Graph for the calculated ADL indicator data, saved.

Simulation Data:
            signal open_trading_action  ... earnings  balance
Date                                   ...
1998-10-05   hold                none  ...        0        0
1998-10-06    buy                long  ...        0  385.138
1998-10-07    buy                long  ...   13.264  411.666
1998-10-08    buy                long  ...   13.264  777.644
1998-10-09    buy                long  ...   19.159  795.329
...           ...                 ...  ...      ...      ...
2020-11-30    buy                long  ...  19817.2  37577.2
2020-12-01   hold                none  ...  19817.2  37577.2
2020-12-02    buy                long  ...  19817.2  38019.2
2020-12-03    buy                long  ...  19817.2  38385.1
2020-12-04    buy                long  ...  19817.2  38837.2

[5651 rows x 7 columns]

Simulation Statistics:
 {'number_of_trading_days': 5651, 'number_of_buy_signals': 4767, 'number_of_ignored_buy_signals': 0, 'number_of_sell_signals': 601, 'number_of_ignored_sell_signals': 0, 'last_stock_value': 475.5, 'last_exposure': 22340.73, 'last_open_long_positions': 40, 'last_open_short_positions': 0, 'last_portfolio_value': 19020.0, 'last_earnings': 19817.21, 'final_balance': 38837.21}

Graph for the executed trading signal simulation, saved.

### tti utils examples

- Graph ./figures/example_data_missing_1.png saved.
- Graph ./figures/example_data_missing_2.png saved.
- Graph ./figures/example_data_missing_3.png saved.