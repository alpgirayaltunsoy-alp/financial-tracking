# Financial Analysis Pro - User Guide

## 🚀 Professional Desktop Financial Analysis Application

### Features:
✅ Real-time stock data fetching using requests
✅ Advanced candlestick charts with multiple timeframes
✅ 15+ Technical indicators (RSI, MACD, Bollinger Bands, Stochastic, ATR, OBV, etc.)
✅ Support & Resistance levels with Pivot Points
✅ Portfolio management with P&L tracking
✅ Comprehensive technical analysis reports
✅ Auto-refresh functionality
✅ Professional dark theme UI

---

## 📦 Installation

### 1. Install Required Packages:
```bash
pip install -r requirements.txt
```

### 2. Run the Application:
```bash
python financial_analysis_pro.py
```

---

## 🎯 How to Use

### Main Interface:

1. **Symbol Input**: Enter stock ticker (e.g., AAPL, TSLA, MSFT, GOOGL)
2. **Period Selection**: Choose time range (1d to max)
3. **Interval Selection**: Select data interval (1m to 1mo)
4. **Analyze Button**: Click to fetch and analyze data
5. **Auto Refresh**: Enable for automatic updates every 60 seconds

### Tabs:

#### 📈 Price Chart
- **Candlestick Chart**: Green = bullish, Red = bearish
- **Moving Averages**: SMA 20, 50, 200
- **Bollinger Bands**: Gray bands showing volatility
- **MACD**: Momentum indicator
- **RSI**: Relative Strength Index (overbought/oversold)
- **Volume**: Trading volume bars

#### 📊 Indicators
- **Stochastic Oscillator**: %K and %D lines
- **ATR**: Average True Range (volatility measure)
- **OBV**: On Balance Volume (volume trend)
- **Returns Distribution**: Daily returns histogram

#### 🎯 Technical Analysis
Comprehensive report including:
- Price action summary
- Moving average analysis
- Trend identification
- Momentum indicators (RSI, MACD, Stochastic)
- Volatility metrics
- Support/Resistance levels (Pivot Points)
- Trading signals
- Risk metrics
- Overall recommendation

#### 💼 Portfolio
Track your positions:
1. Enter number of shares owned
2. Enter your buy price
3. Click "Calculate P&L"

Shows:
- Current position value
- Unrealized P&L (profit/loss)
- ROI percentage
- Daily performance
- Risk analysis
- Profit targets (+5%, +10%, +15%, etc.)
- Stop loss levels (-5%, -10%, -15%, etc.)

#### 📋 Data Table
- Raw price data in table format
- Last 100 data points
- Color-coded: Green = up, Red = down

---

## 🔍 Technical Indicators Explained

### Moving Averages
- **SMA 20**: 20-period simple moving average (short-term trend)
- **SMA 50**: 50-period simple moving average (medium-term trend)
- **SMA 200**: 200-period simple moving average (long-term trend)

### RSI (Relative Strength Index)
- **Above 70**: Overbought (potential sell signal)
- **Below 30**: Oversold (potential buy signal)
- **Between 30-70**: Neutral zone

### MACD (Moving Average Convergence Divergence)
- **MACD Line**: 12-period EMA - 26-period EMA
- **Signal Line**: 9-period EMA of MACD
- **Histogram**: MACD - Signal
- **Bullish**: MACD crosses above Signal
- **Bearish**: MACD crosses below Signal

### Bollinger Bands
- **Upper Band**: Price + (2 × Standard Deviation)
- **Middle Band**: 20-period SMA
- **Lower Band**: Price - (2 × Standard Deviation)
- **Price at upper band**: Potentially overbought
- **Price at lower band**: Potentially oversold

### Stochastic Oscillator
- **%K Line**: Current position relative to high/low range
- **%D Line**: 3-period moving average of %K
- **Above 80**: Overbought
- **Below 20**: Oversold

### ATR (Average True Range)
- Measures volatility
- Higher ATR = Higher volatility
- Used for stop loss placement

### OBV (On Balance Volume)
- Volume-based indicator
- Rising OBV + Rising Price = Strong uptrend
- Falling OBV + Falling Price = Strong downtrend

---

## 📊 Trading Signals Guide

### Bullish Signals (BUY):
✅ RSI < 30 (Oversold)
✅ MACD crosses above Signal line
✅ Price above SMA 20 and SMA 50
✅ Stochastic < 20 (Oversold)
✅ Price at lower Bollinger Band

### Bearish Signals (SELL):
❌ RSI > 70 (Overbought)
❌ MACD crosses below Signal line
❌ Price below SMA 20 and SMA 50
❌ Stochastic > 80 (Overbought)
❌ Price at upper Bollinger Band

### Overall Recommendations:
- **STRONG BUY**: 4-5 bullish signals
- **BUY**: 3 bullish signals
- **HOLD**: Equal signals or neutral
- **SELL**: 3 bearish signals
- **STRONG SELL**: 4-5 bearish signals

---

## 💡 Tips & Best Practices

1. **Multiple Timeframes**: Check both daily and weekly charts
2. **Confirm Signals**: Don't rely on single indicator
3. **Volume Confirmation**: High volume confirms trend
4. **Support/Resistance**: Use pivot points for entry/exit
5. **Risk Management**: Always use stop losses
6. **Diversification**: Don't put all capital in one stock

---

## 🎨 Color Coding

- **Green (#00ff88)**: Bullish/Positive/Up
- **Red (#ff4444)**: Bearish/Negative/Down
- **Orange**: Warning/Caution
- **Purple**: Special indicators (RSI, Stochastic)
- **Blue**: Information/Neutral

---

## 🔄 Data Sources

The application uses Yahoo Finance API to fetch:
- Real-time price data
- Historical OHLCV data
- Company metadata
- Market statistics

Data is fetched via HTTP requests without requiring API keys.

---

## ⚠️ Disclaimer

This application is for educational and informational purposes only.
It is NOT financial advice. Always:
- Do your own research (DYOR)
- Consult with qualified financial advisors
- Never invest more than you can afford to lose
- Past performance does not guarantee future results

---

## 🛠️ Troubleshooting

### "Failed to fetch data" error:
- Check internet connection
- Verify ticker symbol is correct
- Try different period/interval
- Wait a few seconds and retry

### Application runs slowly:
- Reduce data period (use shorter timeframe)
- Close other applications
- Disable auto-refresh if not needed

### Charts not displaying:
- Ensure matplotlib is installed correctly
- Update tkinter if needed
- Restart the application

---

## 📞 Support

For issues or questions:
1. Check this guide thoroughly
2. Verify all dependencies are installed
3. Ensure you have stable internet connection
4. Try with different stock symbols

---

## 🔮 Future Enhancements

Potential features:
- Multiple watchlists
- Custom alerts and notifications
- Backtesting functionality
- Pattern recognition
- Options analysis
- Fundamental data integration
- Export reports to PDF
- Multi-currency support

---

**Version**: 1.0
**Last Updated**: 2024
**Platform**: Python 3.8+

Enjoy professional financial analysis! 📈💰
