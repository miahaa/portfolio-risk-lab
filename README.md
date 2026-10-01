# Portfolio Risk & Analytics Lab

A Python-based quantitative finance project for analyzing stock performance, portfolio risk, diversification, and risk-adjusted returns.

## Overview

This project uses historical market data for **AAPL, MSFT, JPM, JNJ, and NVDA** starting in January 2021. It turns daily price data into portfolio-level risk and performance metrics and visualizations.

The current version uses an equal-weight portfolio, with 20% allocated to each stock.

## Analysis Included

- Daily stock returns
- Annualized returns
- Annualized volatility
- Sharpe ratios
- Maximum drawdowns
- Stock return correlations
- Annualized covariance matrix
- Equal-weight portfolio construction
- Portfolio return and volatility
- Portfolio Sharpe ratio
- Growth of a $10,000 investment
- Portfolio drawdown analysis

## Why This Project Matters

Looking only at return can hide a large part of an investment's risk.

This project compares return with volatility, drawdown, correlation, and risk-adjusted performance. It also demonstrates how combining assets that are not perfectly correlated can reduce portfolio volatility.

## Visualizations

### Growth of $10,000

![Portfolio Growth](images/portfolio_growth.png)

### Portfolio Drawdown

![Portfolio Drawdown](images/portfolio_drawdown.png)

### Correlation Matrix

![Correlation Matrix](images/correlation_matrix.png)

## Tech Stack

- Python
- pandas
- NumPy
- Matplotlib
- yfinance

## How to Run

Clone the repository and install the required Python packages:

```bash
pip install yfinance pandas matplotlib numpy
python main.py
```

The script downloads historical market data using yfinance, calculates the portfolio metrics, and generates the analysis output and charts.

## Current Stage

This project is actively being developed. The current version focuses on an equal-weight five-stock portfolio.

Planned improvements include:

- Expand the portfolio to more assets
- Compare equal-weight and optimized portfolios
- Add benchmark comparison
- Add rolling risk metrics
- Improve automated reporting
- Add portfolio optimization and backtesting

## Key Concepts Demonstrated

Portfolio risk · Diversification · Volatility · Sharpe ratio · Drawdown · Correlation · Covariance · Historical market data · Python financial analysis
