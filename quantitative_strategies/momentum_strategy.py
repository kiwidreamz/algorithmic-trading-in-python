import numpy as np
import pandas as pd
import requests
import math
#from scipy import stats
from scipy.stats import percentileofscore as score
import xlsxwriter
from statistics import mean

# Acquiring API Token
from secrets import IEX_CLOUD_API_TOKEN

# Importing list of stocks
stocks = pd.read_csv('sp_500_stocks.csv')

# Portfolio Size
portfolio_size = 1000000

# Executing A Batch API Call

# Function sourced from 
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]   
        
symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

# Building DataFrame
hqm_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
    'One-Year Price Return',
    'One-Year Return Percentile',
    'Six-Month Price Return',
    'Six-Month Return Percentile',
    'Three-Month Price Return',
    'Three-Month Return Percentile',
    'One-Month Price Return',
    'One-Month Return Percentile',
    'HQM Score'
]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)

hqm_dataframe = pd.DataFrame(columns = hqm_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        if symbol == 'HFC' or symbol == 'VIAC' or symbol == 'WLTW':
                continue
        hqm_dataframe = hqm_dataframe.append(
            pd.Series(
            [
                symbol,
                data[symbol]['price'],
                'N/A',
                data[symbol]['stats']['year1ChangePercent'],
                'N/A',
                data[symbol]['stats']['month6ChangePercent'],
                'N/A',
                data[symbol]['stats']['month3ChangePercent'],
                'N/A',
                data[symbol]['stats']['month1ChangePercent'],
                'N/A',
                'N/A'
            ],
                index = hqm_columns
            ),
            ignore_index = True
        )

# Calculating Momentum Percentiles
time_periods = [
    'One-Year',
    'Six-Month',
    'Three-Month',
    'One-Month'
]

hqm_dataframe.dropna(inplace=True)


for row in hqm_dataframe.index:
    for time_period in time_periods:
        change_col = f'{time_period} Price Return'
        percentile_col = f'{time_period} Return Percentile'
        hqm_dataframe.loc[row, percentile_col] = score(hqm_dataframe[change_col], hqm_dataframe.loc[row, change_col])/100

# Calculating the HQM Score
for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)

# Selecting the 50 Best Momentum Stocks
hqm_dataframe.sort_values('HQM Score', ascending = False, inplace = True)
hqm_dataframe = hqm_dataframe[:50]
hqm_dataframe.reset_index(inplace=True, drop=True)

# Calculating the Number of Shares to Buy
position_size = float(portfolio_size)/len(hqm_dataframe.index)
for i in hqm_dataframe.index:
    hqm_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/hqm_dataframe.loc[i, 'Price'])

# Formatting Our Excel Output
writer = pd.ExcelWriter('momentum_strategy.xlsx', engine='xlsxwriter')
hqm_dataframe.to_excel(writer, sheet_name = 'Momentum Strategy', index = False)

# Creating the Formats
background_color = '#0a0a23'
font_color = '#ffffff'

string_template = writer.book.add_format(
        {
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

dollar_template = writer.book.add_format(
        {
            'num_format':'$0.00',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

integer_template = writer.book.add_format(
        {
            'num_format':'0',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

percent_template = writer.book.add_format(
        {
            'num_format':'0.0%',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

column_formats = {
    'A' : ['Ticker', string_template],
    'B' : ['Price', dollar_template],
    'C' : ['Number of Shares to Buy', integer_template],
    'D' : ['One-Year Price Return', percent_template],
    'E' : ['One-Year Return Percentile', percent_template],
    'F' : ['Six-Month Price Return', percent_template],
    'G' : ['Six-Month Return Percentile', percent_template],
    'H' : ['Three-Month Price Return', percent_template],
    'I' : ['Three-Month Return Percentile', percent_template],
    'J' : ['One-Month Price Return', percent_template],
    'K' : ['One-Month Return Percentile', percent_template],
    'L' : ['HQM Score', percent_template]
}

for column in column_formats.keys():
    writer.sheets['Momentum Strategy'].set_column(f'{column}:{column}', 25, column_formats[column][1])
    writer.sheets['Momentum Strategy'].write(f'{column}1', column_formats[column][0], column_formats[column][1])

writer.save()