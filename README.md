# Algorithmic Trading in Python

This repository contains three projects written in python :

-   Equal Weight SP500
-   Momentum Strategy
-   Value Strategy

These projects were created as part of Nick McCullum's (@nickmccullum) course on Algorithmic Trading with Python, which is available at [freeCodeCamp](https://github.com/freeCodeCamp).
Each project used librairies such as numpy, pandas and scipy to manipulate financial data received from an API and dealt accordingly with missing data.

#### Financial Data

Financial data was provided using IEX Cloud's API. Paying for access to real data was outside the scope of this course, so the sandbox version of the API was used.
This means the data is not accurate and can not be used for real-world financial operations. However, this sandbox feature is free and provides correctly formatted data which allows for proper and accurate testing.

## Equal Weight SP500

Python script that calculates how many shares of each SP500 stock you should purchase in order to get an equal-weight version of the index fund, as opposed to a market capitalization weighed index such as the SPDR® S&P 500® ETF Trust.

This project starts with importing the 500 stocks that make up the SP500 index. Our API Token is then acquired from our secrets file.
Batch API Calls are made, in order to get all 500+ stocks in groups of 100. THe calls are parsed, and the stocks are added to a Pandas DataFrame by looping through the tickers and appending them. The number of shares to buy are then calculated, rounded down to the nearest decimal since many brokers do not allow fractional trading.
All the data contained in our list of stocks, price data, market capitalization data and the number of shares are then outputed to an excel file.

## Momentum Strategy

Python script implementing an investing strategy that selects the 50 American stocks with the highest price momentum. Momentum investing means investing in the stocks that have increased the most in price. The course taught two methods to implement this investment strategy. The first calculates the one year price return of stocks. While this is an valid implementation of a momentum investing strategy, it lacks real-world quality. This is because the period of time over which the surge in price happened is unaccounted for in this strategy.

Here is a quote from the course which explains this better than I can :

> Real-world quantitative investment firms differentiate between "high quality" and "low quality" momentum stocks:
>
> -   High-quality momentum stocks show "slow and steady" outperformance over long periods of time
> -   Low-quality momentum stocks might not show any momentum for a long time, and then surge upwards.
>
> The reason why high-quality momentum stocks are preferred is because low-quality momentum can often be cause by short-term news that is unlikely to be repeated in the future (such as an FDA approval for a biotechnology company).

Therefore, instead of just comparing the one year return, the second strategy helps with picking the more stable momentum stocks by selecting stocks from the highest percentiles from four different points in time :

-   1-month price returns
-   3-month price returns
-   6-month price returns
-   1-year price returns

Once the 50 stocks are selected, the number of shares to buy are then calculated, rounded down to the nearest decimal since many brokers do not allow fractional trading. All this data is then outputed to an excel file.

## Value Strategy

Python script implementing an investing strategy that selects the 50 American stocks with the best value metrics. Value investing is an investment strategy that aims to find stocks that are under-valued, meaning they are cheap compared to their intrisic value, calculated through percentiles of measures such as earnings or assets.

As with the previous project, this was implemented in two ways. The first project only looked at the price to earnings ratio. Looking at a single valuation metric is not a sound strategy.

As quoted from the course :

> Every valuation metric has certain flaws.
> For example, the price-to-earnings ratio doesn't work well with stocks with negative earnings.
> Similarly, stocks that buyback their own shares are difficult to value using the price-to-book ratio.
> Investors typically use a composite basket of valuation metrics to build robust quantitative value strategies.

Therefore, a composite basket of valuation metrics was used to build a more robust quantitative value strategy, including :

-   Price-to-earnings ratio
-   Price-to-book ratio
-   Price-to-sales ratio
-   Enterprise Value divided by Earnings Before Interest, Taxes, Depreciation, and Amortization (EV/EBITDA)
-   Enterprise Value divided by Gross Profit (EV/GP)

Some of these metrics were not provided directly by the IEX API, such as EV over EBITDA or EV over GP. We calculated these metrics, as well as value percentiles which then helped us calculate each stocks Robust Value score. Once the 50 stocks are selected, the number of shares to buy are then calculated, rounded down to the nearest decimal since many brokers do not allow fractional trading. All this data is then outputed to an excel file. 
