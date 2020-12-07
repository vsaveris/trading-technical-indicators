Examples
========

Below is an example on how to use the ``tti.indicators`` package API. Time-series Moving Average is used in this example, but similar usage applies for all the indicators. The only differences from other indicators usage are the required columns in the input data (Time-series Moving Average requires only ``close`` price column) and the different input arguments which each indicator may have.


.. code-block:: bash
    :caption: Input data (part of them)

    date        close
    2012-09-12	140.41
    2012-09-11	140.95
    2012-09-10	141.25
    2012-09-07	144.36
    2012-09-06	143.48
    2012-09-05	142.58
    2012-09-04	142.54
    2012-08-31	141.52
    2012-08-30	141.78
    2012-08-29	142.92
    2012-08-28	143.56
    ...


.. code-block:: python
    :caption: Usage example
    
    import pandas as pd
    from tti.indicators import MovingAverage
    
    # Read data from csv file. Set the index to the correct column
    # (dates column)
    df = pd.read_csv('example_data.csv', parse_dates=True, index_col=0)
    
    # Create indicator (Time-Series Moving Average)
    ma_ind = MovingAverage(input_data=df, period=5, ma_type='time_series')
    
    # Get indicator's calculated data
    print('\nTechnical Indicator data:\n', ma_ind.getTiData())
    
    # Get indicator's value for a specific date
    print('\nTechnical Indicator value at 2012-09-06:', ma_ind.getTiValue('2012-09-06'))
    
    # Get the most recent indicator's value
    print('\nMost recent Technical Indicator value:', ma_ind.getTiValue())
    
    # Get signal from indicator
    print('\nTechnical Indicator signal:', ma_ind.getTiSignal())
    
    # Show the Graph for the calculated Technical Indicator
    ma_ind.getTiGraph().show()
    
    # Save the Graph for the calculated Technical Indicator
    ma_ind.getTiGraph().savefig('example_MovingAverage.png')
    print('Graph saved.')
    
    
.. code-block:: bash
    :caption: Output
    
    Technical Indicator data:
                       ma-time_series
    date
    2012-01-17             NaN
    2012-01-18             NaN
    2012-01-19             NaN
    2012-01-20             NaN
    2012-01-23         128.822
    ...                    ...
    2012-09-06         143.718
    2012-09-07         144.882
    2012-09-10         142.602
    2012-09-11         140.877
    2012-09-12         139.225
    
    Technical Indicator value at 2012-09-06: [143.718]
    
    Most recent Technical Indicator value: [139.225]

    Technical Indicator signal: ('hold', 0)
    
    Graph saved.
    
    
.. image:: ./images/example_MovingAverage_time_series.png
    :align: center
    :width: 400px