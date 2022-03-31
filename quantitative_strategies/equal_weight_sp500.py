import numpy as np
import pandas as pd
import requests 
import xlsxwriter
import math

# Acquiring API Token
from secrets import IEX_CLOUD_API_TOKEN

# Importing list of stocks
stocks = pd.read_csv('sp_500_stocks.csv')

# Portfolio Size
portfolio_size = 1000000

# Adding Stocks Data to a Pandas DataFrame
my_columns = [ 'Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns = my_columns)

# Looping Through The Tickers in List of Stocks
final_dataframe = pd.DataFrame(columns = my_columns)
for stock in stocks['Ticker']:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()
    final_dataframe = final_dataframe.append(
        pd.Series(
        [
            stock,
            data['latestPrice'],
            data['marketCap'],
            'N/A'
        ],
        index = my_columns
        ),
        ignore_index = True
    )

# Using Batch API Calls to Improve Performance
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range (0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

final_dataframe = pd.DataFrame(columns = my_columns)

for symbol_string in symbol_strings:
        batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batch_api_call_url).json()
        for symbol in symbol_string.split(','):
            if symbol == 'HFC' or symbol == 'VIAC' or symbol == 'WLTW':
                continue
            final_dataframe = final_dataframe.append(
            pd.Series(
            [
                symbol,
                data[symbol]['quote']['latestPrice'],
                data[symbol]['quote']['marketCap'],
                'N/A'
            ],
            index = my_columns
            ),
                ignore_index=True
            )

# Calculating the Number of Shares to Buy
val = float(portfolio_size)
position_size = val/len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])

# Formatting Excel Output

# Initializing XlsxWriter Object
writer = pd.ExcelWriter('recommended trades.xlsx', engine ="xlsxwriter")
final_dataframe.to_excel(writer, 'Recommended Trades', index = False)

# Creating the Formats
background_color = '#50c878'
font_color = '#ffffff'

string_format = writer.book.add_format(
    {
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)

dollar_format = writer.book.add_format(
    {
        'num_format': '$0.00',
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)

integer_format = writer.book.add_format(
    {
        'num_format': '0',
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)

# Applying the Formats to the Columns

column_formats = {
    'A': ['Ticker', string_format],
    'B': ['Stock Price', dollar_format],
    'C': ['Market Capitalization', dollar_format],
    'D': ['Number of Shares to Buy', integer_format]
}

for column in column_formats.keys():
    writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 18, column_formats[column][1])
    writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], column_formats[column][1])
    
writer.save()
