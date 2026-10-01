import yfinance as yf # use yfinance to retrieve historical stock data
import pandas as pd   # table of data 
import matplotlib.pyplot as plt   
import numpy as np

tickers = ["AAPL", "MSFT", "JPM", "JNJ", "NVDA"]    # 5 stock companies

# Get historical market data for these five stocks starting January 1, 2021.
data = yf.download(
    tickers,
    start="2021-01-01",
    auto_adjust=True
)

# extracts the closing-price data
prices = data["Close"]

# Show the last 5 rows
print(prices.tail())

# Calculate daily return for financial analysis
# prices.pct_change(): for each stock, pandas essentially calculates: Rt = (Pt - P(t-1)) / P(t-1)
# .dropna(): removes the first row because the first price doesn't have a previous day's price to compare against.
daily_returns = prices.pct_change().dropna()

print("\nDaily Returns:")

# daily return over the last 5 days.
print(daily_returns.tail())

# average across all daily returns since 2021
print(daily_returns.mean())
average_daily_return = daily_returns.mean()

# Annualize the return 
# There are approximately 252 trading days per year.
# Annualized return = Average daily return x 252
annual_returns = average_daily_return * 252
print("\nAnnualized Returns:")
print(annual_returns)

# VOLATILITY
# Return tells us how much the investment earned.
# Volatility tells us how much those returns move around.
# use .std() to calculate deviation
daily_volatility = daily_returns.std()
# Annualize daily volatility
annual_volatility = daily_volatility * (252 ** 0.5)
# Print
print("\nAnnualized Volatility:")
print(annual_volatility)

# Sharpe ratio
# How much excess return am I getting for the risk I'm taking?
# Sharpe = (Annualized Return - Risk Free Rate) / Annualized Volatility
# Assume risk free rate is 4%
risk_free_rate = 0.04
sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility
print("\nSharpe Ratios:")
print(sharpe_ratio)

# Peak price
# The returns are compounded day by day
cumulative_returns = (1 + daily_returns).cumprod()
running_peak = cumulative_returns.cummax()

# Drawdown
drawdown = (cumulative_returns - running_peak) / running_peak
print("\ndrawdown:")
# print(drawdown)

# Maximum Drawdown
max_drawdown = drawdown.min()
print("\nMaximum Drawdown:")
print(max_drawdown)

# From the data, NVDA had the strongest return in your sample, but it also experienced the deepest historical decline.
# For example:
#   - NVDA annualized return: about 62.8%
#   - NVDA annualized volatility: about 50.6%
#   - NVDA max drawdown: about -66.3%
#   - NVDA Sharpe ratio: about 1.16
# So someone looking only at return would miss a huge part of the story.


# CORRELATION
# Correlation tells us how two stocks tend to move relative to each other.
# Correlation near +1 → tend to move in the same direction
# Correlation near 0 → weak relationship
# Correlation near -1 → tend to move in opposite directions
correlation_matrix = daily_returns.corr()  # Correlation func
print("\nCorrelation matrix:")
print(correlation_matrix)

# # Correlation heatmap
# fig, ax = plt.subplots(figsize=(8, 6))

# heatmap = ax.imshow(correlation_matrix)

# ax.set_xticks(range(len(tickers)))
# ax.set_yticks(range(len(tickers)))

# ax.set_xticklabels(tickers)
# ax.set_yticklabels(tickers)

# plt.title("Stock Return Correlation Matrix")
# plt.colorbar(heatmap)

# # Label each square, loop through the matrix 
# for i in range(len(tickers)):
#     for j in range(len(tickers)):
#         value = correlation_matrix.iloc[i, j]

#         ax.text(
#             j,
#             i,
#             f"{value:.2f}",       # Display the number using two decimal places.
#             ha="center",
#             va="center"
#         )

# plt.savefig("images/correlation_matrix.png", dpi=300, bbox_inches="tight")
# plt.show()


# PORTFOLIO WEIGHTS
""" 
Right now we're analyzing:
tickers = ["AAPL", "MSFT", "JPM", "JNJ", "NVDA"]
We'll start with an equal-weight portfolio. With 5 stocks: Weight = 1/5 = 20%
So each stock gets 20%.
"""
num_assets = len(tickers)

weights = np.array([1 / num_assets] * num_assets)

print("\nPortfolio Weights:")
print(weights)

# The portfolio return is: Rp = w1R1 + w2R2 + ... + wnRn
portfolio_return = sum(weights * annual_returns)
print("\nPortfolio Annualized Return:")
print(portfolio_return)
print(f"Portfolio Annualized Return: {portfolio_return:.2%}")
