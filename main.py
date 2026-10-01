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
# print(prices.tail())

# Calculate daily return for financial analysis
# prices.pct_change(): for each stock, pandas essentially calculates: Rt = (Pt - P(t-1)) / P(t-1)
# .dropna(): removes the first row because the first price doesn't have a previous day's price to compare against.
daily_returns = prices.pct_change().dropna()

# print("\nDaily Returns:")

# daily return over the last 5 days.
# print(daily_returns.tail())

# average across all daily returns since 2021
# print(daily_returns.mean())
average_daily_return = daily_returns.mean()

# Annualize the return 
# There are approximately 252 trading days per year.
# Annualized return = Average daily return x 252
annual_returns = average_daily_return * 252
# print("\nAnnualized Returns:")
# print(annual_returns)

# VOLATILITY
# Return tells us how much the investment earned.
# Volatility tells us how much those returns move around.
# use .std() to calculate deviation
daily_volatility = daily_returns.std()
# Annualize daily volatility
annual_volatility = daily_volatility * (252 ** 0.5)
# Print
# print("\nAnnualized Volatility:")
# print(annual_volatility)

# Sharpe ratio
# How much excess return am I getting for the risk I'm taking?
# Sharpe = (Annualized Return - Risk Free Rate) / Annualized Volatility
# Assume risk free rate is 4%
risk_free_rate = 0.04
sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility
# print("\nSharpe Ratios:")
# print(sharpe_ratio)

# Peak price
# The returns are compounded day by day
cumulative_returns = (1 + daily_returns).cumprod()
running_peak = cumulative_returns.cummax()

# Drawdown
drawdown = (cumulative_returns - running_peak) / running_peak
# print("\ndrawdown:")
# print(drawdown)

# Maximum Drawdown
max_drawdown = drawdown.min()
# print("\nMaximum Drawdown:")
# print(max_drawdown)

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
# print("\nCorrelation matrix:")
# print(correlation_matrix)

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

# print("\nPortfolio Weights:")
# print(weights)

# The portfolio return is: Rp = w1R1 + w2R2 + ... + wnRn
portfolio_return = sum(weights * annual_returns)
# print("\nPortfolio Annualized Return:")
# print(portfolio_return)
# print(f"Portfolio Annualized Return: {portfolio_return:.2%}")

# Portfolio volatility
covariance_matrix = daily_returns.cov() * 252

# print("\nAnnualized Covariance Matrix:")
# print(covariance_matrix)

# Calculate portfolio variance
portfolio_variance = weights.T @ covariance_matrix @ weights

portfolio_volatility = np.sqrt(portfolio_variance)

# print(f"\nPortfolio Annualized Volatility: {portfolio_volatility:.2%}")

'''
Portfolio volatility is 20.29%, while the portfolio's expected annualized return is 27.80%.
=> Clear demonstration of diversification: several individual stocks have much higher volatility, such as NVDA at 50.63%, 
but combining assets whose returns aren't perfectly correlated brings the portfolio volatility down.
'''

# Portfolio Sharpe Ratio
# Use the same formula as for Sharpe
portfolio_sharpe = (portfolio_return - risk_free_rate) / portfolio_volatility
print(f"Portfolio Sharpe Ratio: {portfolio_sharpe:.2f}")

# Create portfolio performance summary
portfolio_summary = pd.Series({
    "Annualized Return": portfolio_return,
    "Annualized Volatility": portfolio_volatility,
    "Sharpe Ratio": portfolio_sharpe
})

print("\nPortfolio Summary:")
print(f"Annualized Return: {portfolio_return:.2%}")
print(f"Annualized Volatility: {portfolio_volatility:.2%}")
print(f"Sharpe Ratio: {portfolio_sharpe:.2f}")

# Calculate the portfolio's daily returns
# It can be calculated by the sum of daily return of each stocks multiply with weight of each 
portfolio_daily_returns = daily_returns @ weights # @ performs matrix multiplication.

# print("\nPortfolio Daily Returns:")
# print(portfolio_daily_returns.tail())


# Calculate cumulative portfolio performance
portfolio_cumulative = (1 + portfolio_daily_returns).cumprod()

# print("\nPortfolio Cumulative Performance:")
# print(portfolio_cumulative.tail())

# Create a Growth of #10,000 chart 
initial_investment = 10000

portfolio_value = initial_investment * portfolio_cumulative
print(f"\nFinal Portfolio Value: ${portfolio_value.iloc[-1]:,.2f}") # :,.2f is to turn something like 25342.827 into 25,342.83

# Create the chart 
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(portfolio_value.index, portfolio_value)

ax.set_title("Growth of $10,000 - Equal-Weight Portfolio")
ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Value ($)")
ax.grid(True, alpha=0.3)

plt.tight_layout()
# plt.savefig("images/correlation_matrix.png", dpi=300, bbox_inches="tight")
# plt.savefig(
#     "images/portfolio_growth.png",
#     dpi=300,
#     bbox_inches="tight"
# )
# plt.show()

# Calculate portfolio maximum drawdown
portfolio_running_peak = portfolio_cumulative.cummax()

portfolio_drawdown = (
    portfolio_cumulative - portfolio_running_peak
) / portfolio_running_peak

portfolio_max_drawdown = portfolio_drawdown.min()

print(f"\nPortfolio Maximum Drawdown: {portfolio_max_drawdown:.2%}")

# Draw chart 
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(portfolio_drawdown.index, portfolio_drawdown)

ax.set_title("Portfolio Drawdown")
ax.set_xlabel("Date")
ax.set_ylabel("Drawdown")
ax.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "images/portfolio_drawdown.png",
    dpi=300,
    bbox_inches="tight"
)

# plt.show()

'''
S&P 500 benchmarking: Did my portfolio actually outperform the market, and was the extra return worth the extra risk?
We'll use the S&P 500 as our market benchmark. With yfinance, its ticker is: ^GSPC
'''
# BENCHMARK
# Use the S&P 500 as the market benchmark
benchmark = yf.download(
    "^GSPC",                     # ^GSPC represents the S&P 500 index.
    start="2021-01-01",
    auto_adjust=True
)

benchmark_prices = benchmark["Close"]   # extracts the closing-price series

# Calculate daily S&P 500 returns
benchmark_daily_returns = benchmark_prices.pct_change().dropna() # pct_change() calculates daily return automatically for every trading day.

print("\nS&P 500 Daily Returns:")
print(benchmark_daily_returns.tail())

# print("\nS&P 500 Prices:")
# print(benchmark_prices.tail())

# Calculate annualized S&P 500 return
"""
This is an arithmetic annualized return, not the same thing as CAGR.
- Annualized arithmetic return estimates the average yearly return from daily observations.
- CAGR measures the compounded growth rate from the beginning to the end.
"""
benchmark_annual_return = benchmark_daily_returns["^GSPC"].mean() * 252

# print("\nS&P 500 Annualized Return:")
# print(benchmark_annual_return)

# Calculate the S&P 500 volatility from its daily returns
benchmark_volatility = benchmark_daily_returns["^GSPC"].std() * np.sqrt(252)

print(f"S&P 500 Annualized Volatility: {benchmark_volatility:.2%}")

# Compare portfolio performance against the S&P 500
excess_return = portfolio_return - benchmark_annual_return

print("\nPERFORMANCE VS S&P 500")
print(f"Portfolio Annualized Return: {portfolio_return:.2%}") # :.2% converts 0.14067 to 14.07%
print(f"S&P 500 Annualized Return: {benchmark_annual_return:.2%}")
print(f"Excess Return: {excess_return:.2%}")

print("\nRISK VS S&P 500")
print(f"Portfolio Annualized Volatility: {portfolio_volatility:.2%}")
print(f"S&P 500 Annualized Volatility: {benchmark_volatility:.2%}")

# Calculate benchmark Sharpe ratio
benchmark_sharpe = (
    benchmark_annual_return - risk_free_rate
) / benchmark_volatility

print(f"S&P 500 Sharpe Ratio: {benchmark_sharpe:.2f}")

"""
A higher Sharpe ratio means you earned more excess return per unit of risk.
So if:
Portfolio Sharpe: 1.10
S&P 500 Sharpe:   0.65
portfolio had stronger risk-adjusted performance under this model.
"""
print("\nRISK-ADJUSTED PERFORMANCE")
print(f"Portfolio Sharpe Ratio: {portfolio_sharpe:.2f}")
print(f"S&P 500 Sharpe Ratio: {benchmark_sharpe:.2f}")


'''
Beta: How sensitive is your portfolio to movements in the overall stock market?
Beta = 1.00 → tends to move with the market
Beta > 1.00 → more sensitive to market movements
Beta < 1.00 → less sensitive to market movements
Beta < 0    → tends to move opposite the market
'''
# Align portfolio and benchmark returns by date
comparison_data = pd.concat(
    [
        portfolio_daily_returns.rename("Portfolio"),
        benchmark_daily_returns["^GSPC"].rename("Market")
    ],
    axis=1
).dropna()

# print("\nAligned Portfolio and Market Returns:")
# print(comparison_data.tail())

# Calculate portfolio beta relative to the S&P 500
covariance_with_market = comparison_data["Portfolio"].cov(
    comparison_data["Market"]
)

market_variance = comparison_data["Market"].var()

portfolio_beta = covariance_with_market / market_variance

print(f"\nPortfolio Beta: {portfolio_beta:.2f}")


'''
Given that my portfolio took more systematic market risk, how much return should I have expected?
CAPM Expected Return (Capital Asset Pricing Model) can be calculated: risk_free_rate + beta * (market_return - risk_free_rate)
'''
# CAPM expected return
capm_expected_return = (
    risk_free_rate
    + portfolio_beta * (benchmark_annual_return - risk_free_rate)
)

print(f"CAPM Expected Return: {capm_expected_return:.2%}")

# Calculate Jensen's Alpha: the difference between portfolio annualized return and CAPM expected return
portfolio_alpha = portfolio_annual_return - capm_expected_return

print(f"Jensen's Alpha: {portfolio_alpha:.2%}")