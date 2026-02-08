"""
Professional Financial Analysis Application
Desktop-based with real-time data using requests
All professional trading tools included
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import json
import threading
import time

class FinancialAnalysisPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Analysis Pro - Real-time Trading Platform")
        self.root.geometry("1600x900")
        self.root.configure(bg='#0a0e27')
        
        # Data storage
        self.current_data = None
        self.current_symbol = "AAPL"
        self.auto_refresh = False
        self.refresh_interval = 60  # seconds
        
        # Style configuration
        self.setup_styles()
        
        # Create main interface
        self.create_interface()
        
        # Load initial data
        self.fetch_data()
    
    def setup_styles(self):
        """Configure custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#0a0e27'
        fg_color = '#e0e0e0'
        accent_color = '#00ff88'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
        style.configure('Header.TLabel', background=bg_color, foreground=accent_color, font=('Arial', 14, 'bold'))
        style.configure('TButton', background='#1e2139', foreground=fg_color, font=('Arial', 10, 'bold'))
        style.configure('Accent.TButton', background='#00ff88', foreground='#0a0e27', font=('Arial', 10, 'bold'))
        style.configure('TEntry', fieldbackground='#1e2139', foreground=fg_color, font=('Arial', 10))
        style.configure('TNotebook', background=bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background='#1e2139', foreground=fg_color, padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', '#2e3350')])
    
    def create_interface(self):
        """Create main interface"""
        # Top control panel
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Symbol input
        ttk.Label(control_frame, text="Symbol:").pack(side=tk.LEFT, padx=5)
        self.symbol_entry = ttk.Entry(control_frame, width=10)
        self.symbol_entry.insert(0, self.current_symbol)
        self.symbol_entry.pack(side=tk.LEFT, padx=5)
        
        # Period selection
        ttk.Label(control_frame, text="Period:").pack(side=tk.LEFT, padx=5)
        self.period_var = tk.StringVar(value="1y")
        periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"]
        period_combo = ttk.Combobox(control_frame, textvariable=self.period_var, values=periods, width=8, state='readonly')
        period_combo.pack(side=tk.LEFT, padx=5)
        
        # Interval selection
        ttk.Label(control_frame, text="Interval:").pack(side=tk.LEFT, padx=5)
        self.interval_var = tk.StringVar(value="1d")
        intervals = ["1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"]
        interval_combo = ttk.Combobox(control_frame, textvariable=self.interval_var, values=intervals, width=8, state='readonly')
        interval_combo.pack(side=tk.LEFT, padx=5)
        
        # Analyze button
        analyze_btn = ttk.Button(control_frame, text="📊 ANALYZE", style='Accent.TButton', command=self.analyze)
        analyze_btn.pack(side=tk.LEFT, padx=10)
        
        # Auto-refresh
        self.auto_refresh_var = tk.BooleanVar(value=False)
        auto_refresh_check = ttk.Checkbutton(control_frame, text="Auto Refresh (60s)", variable=self.auto_refresh_var, command=self.toggle_auto_refresh)
        auto_refresh_check.pack(side=tk.LEFT, padx=10)
        
        # Status
        self.status_label = ttk.Label(control_frame, text="Ready", foreground='#00ff88')
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Metrics panel
        metrics_frame = ttk.Frame(self.root)
        metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.metric_labels = {}
        metric_names = [
            ("Current Price", "price"),
            ("Change", "change"),
            ("Change %", "change_pct"),
            ("Volume", "volume"),
            ("Market Cap", "market_cap"),
            ("P/E Ratio", "pe_ratio"),
            ("52W High", "high_52w"),
            ("52W Low", "low_52w")
        ]
        
        for i, (name, key) in enumerate(metric_names):
            frame = ttk.Frame(metrics_frame, relief=tk.RAISED, borderwidth=1)
            frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text=name, font=('Arial', 8)).pack()
            self.metric_labels[key] = ttk.Label(frame, text="--", font=('Arial', 12, 'bold'))
            self.metric_labels[key].pack()
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_chart_tab()
        self.create_indicators_tab()
        self.create_technical_tab()
        self.create_portfolio_tab()
        self.create_data_tab()
    
    def create_chart_tab(self):
        """Create price chart tab"""
        chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(chart_frame, text="📈 Price Chart")
        
        # Create matplotlib figure
        self.fig_chart = Figure(figsize=(14, 8), facecolor='#0a0e27')
        self.canvas_chart = FigureCanvasTkAgg(self.fig_chart, chart_frame)
        self.canvas_chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_indicators_tab(self):
        """Create technical indicators tab"""
        indicators_frame = ttk.Frame(self.notebook)
        self.notebook.add(indicators_frame, text="📊 Indicators")
        
        self.fig_indicators = Figure(figsize=(14, 8), facecolor='#0a0e27')
        self.canvas_indicators = FigureCanvasTkAgg(self.fig_indicators, indicators_frame)
        self.canvas_indicators.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_technical_tab(self):
        """Create technical analysis tab"""
        technical_frame = ttk.Frame(self.notebook)
        self.notebook.add(technical_frame, text="🎯 Technical Analysis")
        
        # Create text widget for analysis
        text_frame = ttk.Frame(technical_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.technical_text = tk.Text(text_frame, bg='#1e2139', fg='#e0e0e0', font=('Courier', 10), yscrollcommand=scrollbar.set)
        self.technical_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.technical_text.yview)
    
    def create_portfolio_tab(self):
        """Create portfolio management tab"""
        portfolio_frame = ttk.Frame(self.notebook)
        self.notebook.add(portfolio_frame, text="💼 Portfolio")
        
        # Input section
        input_frame = ttk.Frame(portfolio_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Shares:").pack(side=tk.LEFT, padx=5)
        self.shares_entry = ttk.Entry(input_frame, width=10)
        self.shares_entry.insert(0, "0")
        self.shares_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(input_frame, text="Buy Price ($):").pack(side=tk.LEFT, padx=5)
        self.buy_price_entry = ttk.Entry(input_frame, width=10)
        self.buy_price_entry.insert(0, "0.00")
        self.buy_price_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Calculate P&L", command=self.calculate_portfolio).pack(side=tk.LEFT, padx=10)
        
        # Results section
        results_frame = ttk.Frame(portfolio_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.portfolio_text = tk.Text(results_frame, bg='#1e2139', fg='#e0e0e0', font=('Courier', 12), height=20)
        self.portfolio_text.pack(fill=tk.BOTH, expand=True)
    
    def create_data_tab(self):
        """Create raw data tab"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="📋 Data Table")
        
        # Create treeview for data display
        tree_frame = ttk.Frame(data_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Change %"]
        self.data_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', 
                                      yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=120)
        
        self.data_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar_y.config(command=self.data_tree.yview)
        scrollbar_x.config(command=self.data_tree.xview)
    
    def fetch_data(self):
        """Fetch real-time data using requests"""
        symbol = self.symbol_entry.get().upper()
        period = self.period_var.get()
        interval = self.interval_var.get()
        
        self.status_label.config(text=f"Fetching data for {symbol}...", foreground='#ffaa00')
        self.root.update()
        
        try:
            # Calculate date range
            end_date = datetime.now()
            period_map = {
                "1d": 1, "5d": 5, "1mo": 30, "3mo": 90,
                "6mo": 180, "1y": 365, "2y": 730, "5y": 1825, "max": 3650
            }
            days = period_map.get(period, 365)
            start_date = end_date - timedelta(days=days)
            
            # Use Yahoo Finance API alternative (yfinance backend)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                "period1": int(start_date.timestamp()),
                "period2": int(end_date.timestamp()),
                "interval": interval,
                "events": "div,split"
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                
                # Extract price data
                timestamps = result['timestamp']
                quotes = result['indicators']['quote'][0]
                
                # Create DataFrame
                df = pd.DataFrame({
                    'Date': [datetime.fromtimestamp(ts) for ts in timestamps],
                    'Open': quotes['open'],
                    'High': quotes['high'],
                    'Low': quotes['low'],
                    'Close': quotes['close'],
                    'Volume': quotes['volume']
                })
                
                # Remove NaN values
                df = df.dropna()
                
                # Get metadata
                meta = result['meta']
                
                # Calculate additional metrics
                df = self.calculate_indicators(df)
                
                self.current_data = {
                    'df': df,
                    'meta': meta,
                    'symbol': symbol
                }
                
                self.current_symbol = symbol
                self.status_label.config(text=f"Data loaded successfully for {symbol}", foreground='#00ff88')
                
                return True
            else:
                raise Exception("No data received")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")
            self.status_label.config(text="Error fetching data", foreground='#ff4444')
            return False
    
    def calculate_indicators(self, df):
        """Calculate technical indicators"""
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # ATR
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['ATR'] = true_range.rolling(14).mean()
        
        # Stochastic Oscillator
        low_14 = df['Low'].rolling(window=14).min()
        high_14 = df['High'].rolling(window=14).max()
        df['Stoch_K'] = 100 * ((df['Close'] - low_14) / (high_14 - low_14))
        df['Stoch_D'] = df['Stoch_K'].rolling(window=3).mean()
        
        # OBV
        df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
        
        # Daily Returns
        df['Returns'] = df['Close'].pct_change()
        
        return df
    
    def analyze(self):
        """Main analysis function"""
        if self.fetch_data():
            self.update_metrics()
            self.plot_price_chart()
            self.plot_indicators()
            self.generate_technical_analysis()
            self.update_data_table()
    
    def update_metrics(self):
        """Update metric labels"""
        if self.current_data is None:
            return
        
        df = self.current_data['df']
        meta = self.current_data['meta']
        
        current_price = df['Close'].iloc[-1]
        prev_close = meta.get('chartPreviousClose', df['Close'].iloc[-2])
        change = current_price - prev_close
        change_pct = (change / prev_close) * 100
        
        # Update labels
        self.metric_labels['price'].config(text=f"${current_price:.2f}")
        
        change_color = '#00ff88' if change >= 0 else '#ff4444'
        self.metric_labels['change'].config(text=f"${change:+.2f}", foreground=change_color)
        self.metric_labels['change_pct'].config(text=f"{change_pct:+.2f}%", foreground=change_color)
        
        self.metric_labels['volume'].config(text=f"{df['Volume'].iloc[-1]:,.0f}")
        
        market_cap = meta.get('marketCap', 0)
        if market_cap > 0:
            if market_cap >= 1e12:
                mc_str = f"${market_cap/1e12:.2f}T"
            elif market_cap >= 1e9:
                mc_str = f"${market_cap/1e9:.2f}B"
            elif market_cap >= 1e6:
                mc_str = f"${market_cap/1e6:.2f}M"
            else:
                mc_str = f"${market_cap:,.0f}"
        else:
            mc_str = "N/A"
        self.metric_labels['market_cap'].config(text=mc_str)
        
        # P/E Ratio
        pe_ratio = meta.get('trailingPE', 0)
        self.metric_labels['pe_ratio'].config(text=f"{pe_ratio:.2f}" if pe_ratio else "N/A")
        
        # 52-week high/low
        high_52w = df['High'].tail(252).max() if len(df) >= 252 else df['High'].max()
        low_52w = df['Low'].tail(252).min() if len(df) >= 252 else df['Low'].min()
        
        self.metric_labels['high_52w'].config(text=f"${high_52w:.2f}")
        self.metric_labels['low_52w'].config(text=f"${low_52w:.2f}")
    
    def plot_price_chart(self):
        """Plot candlestick chart with indicators"""
        if self.current_data is None:
            return
        
        df = self.current_data['df']
        symbol = self.current_data['symbol']
        
        self.fig_chart.clear()
        
        # Create subplots
        gs = self.fig_chart.add_gridspec(4, 1, height_ratios=[3, 1, 1, 1], hspace=0.1)
        ax1 = self.fig_chart.add_subplot(gs[0])
        ax2 = self.fig_chart.add_subplot(gs[1], sharex=ax1)
        ax3 = self.fig_chart.add_subplot(gs[2], sharex=ax1)
        ax4 = self.fig_chart.add_subplot(gs[3], sharex=ax1)
        
        # Plot 1: Candlestick and Moving Averages
        for idx in range(len(df)):
            row = df.iloc[idx]
            color = '#00ff88' if row['Close'] >= row['Open'] else '#ff4444'
            
            # Draw candlestick
            ax1.plot([row['Date'], row['Date']], [row['Low'], row['High']], color=color, linewidth=1)
            
            body_height = abs(row['Close'] - row['Open'])
            body_bottom = min(row['Open'], row['Close'])
            
            rect = Rectangle((mdates.date2num(row['Date']) - 0.3, body_bottom), 
                           0.6, body_height, facecolor=color, edgecolor=color)
            ax1.add_patch(rect)
        
        # Plot moving averages
        ax1.plot(df['Date'], df['SMA_20'], label='SMA 20', color='orange', linewidth=1, alpha=0.7)
        ax1.plot(df['Date'], df['SMA_50'], label='SMA 50', color='blue', linewidth=1, alpha=0.7)
        ax1.plot(df['Date'], df['SMA_200'], label='SMA 200', color='red', linewidth=1, alpha=0.7)
        
        # Bollinger Bands
        ax1.plot(df['Date'], df['BB_Upper'], 'gray', linewidth=0.5, linestyle='--', alpha=0.5)
        ax1.plot(df['Date'], df['BB_Lower'], 'gray', linewidth=0.5, linestyle='--', alpha=0.5)
        ax1.fill_between(df['Date'], df['BB_Upper'], df['BB_Lower'], alpha=0.1, color='gray')
        
        ax1.set_ylabel('Price ($)', color='white')
        ax1.set_title(f'{symbol} - Technical Analysis', color='white', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper left', framealpha=0.3)
        ax1.grid(True, alpha=0.2)
        ax1.set_facecolor('#0a0e27')
        
        # Plot 2: MACD
        ax2.plot(df['Date'], df['MACD'], label='MACD', color='#00aaff', linewidth=1)
        ax2.plot(df['Date'], df['MACD_Signal'], label='Signal', color='#ff6600', linewidth=1)
        
        colors = ['#00ff88' if val >= 0 else '#ff4444' for val in df['MACD_Hist']]
        ax2.bar(df['Date'], df['MACD_Hist'], color=colors, alpha=0.3, width=0.8)
        
        ax2.set_ylabel('MACD', color='white')
        ax2.axhline(y=0, color='white', linewidth=0.5, alpha=0.5)
        ax2.legend(loc='upper left', framealpha=0.3, fontsize=8)
        ax2.grid(True, alpha=0.2)
        ax2.set_facecolor('#0a0e27')
        
        # Plot 3: RSI
        ax3.plot(df['Date'], df['RSI'], label='RSI', color='#aa00ff', linewidth=1.5)
        ax3.axhline(y=70, color='#ff4444', linewidth=0.8, linestyle='--', alpha=0.7, label='Overbought')
        ax3.axhline(y=30, color='#00ff88', linewidth=0.8, linestyle='--', alpha=0.7, label='Oversold')
        ax3.fill_between(df['Date'], 30, 70, alpha=0.1, color='gray')
        
        ax3.set_ylabel('RSI', color='white')
        ax3.set_ylim(0, 100)
        ax3.legend(loc='upper left', framealpha=0.3, fontsize=8)
        ax3.grid(True, alpha=0.2)
        ax3.set_facecolor('#0a0e27')
        
        # Plot 4: Volume
        colors = ['#00ff88' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#ff4444' 
                 for i in range(len(df))]
        ax4.bar(df['Date'], df['Volume'], color=colors, alpha=0.5, width=0.8)
        
        ax4.set_ylabel('Volume', color='white')
        ax4.set_xlabel('Date', color='white')
        ax4.grid(True, alpha=0.2)
        ax4.set_facecolor('#0a0e27')
        
        # Format x-axis
        for ax in [ax1, ax2, ax3, ax4]:
            ax.tick_params(colors='white')
            plt.setp(ax.spines.values(), color='#2e3350')
        
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)
        
        self.fig_chart.autofmt_xdate()
        self.canvas_chart.draw()
    
    def plot_indicators(self):
        """Plot additional indicators"""
        if self.current_data is None:
            return
        
        df = self.current_data['df']
        
        self.fig_indicators.clear()
        
        # Create 2x2 subplot grid
        axes = self.fig_indicators.subplots(2, 2)
        
        # Stochastic Oscillator
        axes[0, 0].plot(df['Date'], df['Stoch_K'], label='%K', color='#00aaff', linewidth=1.5)
        axes[0, 0].plot(df['Date'], df['Stoch_D'], label='%D', color='#ff6600', linewidth=1.5)
        axes[0, 0].axhline(y=80, color='#ff4444', linewidth=0.8, linestyle='--', alpha=0.5)
        axes[0, 0].axhline(y=20, color='#00ff88', linewidth=0.8, linestyle='--', alpha=0.5)
        axes[0, 0].fill_between(df['Date'], 20, 80, alpha=0.1, color='gray')
        axes[0, 0].set_title('Stochastic Oscillator', color='white', fontweight='bold')
        axes[0, 0].set_ylabel('Value', color='white')
        axes[0, 0].legend(loc='upper left', framealpha=0.3)
        axes[0, 0].grid(True, alpha=0.2)
        axes[0, 0].set_facecolor('#0a0e27')
        
        # ATR
        axes[0, 1].plot(df['Date'], df['ATR'], label='ATR', color='#ff00ff', linewidth=1.5)
        axes[0, 1].fill_between(df['Date'], 0, df['ATR'], alpha=0.3, color='#ff00ff')
        axes[0, 1].set_title('Average True Range (ATR)', color='white', fontweight='bold')
        axes[0, 1].set_ylabel('ATR', color='white')
        axes[0, 1].legend(loc='upper left', framealpha=0.3)
        axes[0, 1].grid(True, alpha=0.2)
        axes[0, 1].set_facecolor('#0a0e27')
        
        # OBV
        axes[1, 0].plot(df['Date'], df['OBV'], label='OBV', color='#00ffff', linewidth=1.5)
        axes[1, 0].fill_between(df['Date'], 0, df['OBV'], alpha=0.3, color='#00ffff')
        axes[1, 0].set_title('On Balance Volume (OBV)', color='white', fontweight='bold')
        axes[1, 0].set_ylabel('OBV', color='white')
        axes[1, 0].set_xlabel('Date', color='white')
        axes[1, 0].legend(loc='upper left', framealpha=0.3)
        axes[1, 0].grid(True, alpha=0.2)
        axes[1, 0].set_facecolor('#0a0e27')
        
        # Returns Distribution
        returns = df['Returns'].dropna() * 100
        axes[1, 1].hist(returns, bins=50, color='#00ff88', alpha=0.7, edgecolor='black')
        axes[1, 1].axvline(x=returns.mean(), color='red', linewidth=2, linestyle='--', label=f'Mean: {returns.mean():.2f}%')
        axes[1, 1].set_title('Daily Returns Distribution', color='white', fontweight='bold')
        axes[1, 1].set_xlabel('Returns (%)', color='white')
        axes[1, 1].set_ylabel('Frequency', color='white')
        axes[1, 1].legend(loc='upper right', framealpha=0.3)
        axes[1, 1].grid(True, alpha=0.2)
        axes[1, 1].set_facecolor('#0a0e27')
        
        # Format all axes
        for ax_row in axes:
            for ax in ax_row:
                ax.tick_params(colors='white')
                plt.setp(ax.spines.values(), color='#2e3350')
        
        self.fig_indicators.tight_layout()
        self.canvas_indicators.draw()
    
    def generate_technical_analysis(self):
        """Generate technical analysis report"""
        if self.current_data is None:
            return
        
        df = self.current_data['df']
        symbol = self.current_data['symbol']
        
        self.technical_text.delete(1.0, tk.END)
        
        report = f"""
{'='*80}
TECHNICAL ANALYSIS REPORT - {symbol}
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
PRICE ACTION
{'='*80}
Current Price:      ${df['Close'].iloc[-1]:.2f}
Previous Close:     ${df['Close'].iloc[-2]:.2f}
Change:             ${df['Close'].iloc[-1] - df['Close'].iloc[-2]:+.2f}
Change %:           {((df['Close'].iloc[-1] / df['Close'].iloc[-2]) - 1) * 100:+.2f}%

High (Today):       ${df['High'].iloc[-1]:.2f}
Low (Today):        ${df['Low'].iloc[-1]:.2f}
Volume:             {df['Volume'].iloc[-1]:,.0f}

{'='*80}
MOVING AVERAGES
{'='*80}
SMA 20:             ${df['SMA_20'].iloc[-1]:.2f}
SMA 50:             ${df['SMA_50'].iloc[-1]:.2f}
SMA 200:            ${df['SMA_200'].iloc[-1]:.2f}

EMA 12:             ${df['EMA_12'].iloc[-1]:.2f}
EMA 26:             ${df['EMA_26'].iloc[-1]:.2f}

"""
        
        # Trend Analysis
        current_price = df['Close'].iloc[-1]
        sma20 = df['SMA_20'].iloc[-1]
        sma50 = df['SMA_50'].iloc[-1]
        sma200 = df['SMA_200'].iloc[-1]
        
        trend = "BULLISH" if current_price > sma20 > sma50 > sma200 else \
                "BEARISH" if current_price < sma20 < sma50 < sma200 else "NEUTRAL"
        
        report += f"""
Trend Signal:       {trend}
Price vs SMA20:     {'ABOVE' if current_price > sma20 else 'BELOW'} ({((current_price/sma20-1)*100):+.2f}%)
Price vs SMA50:     {'ABOVE' if current_price > sma50 else 'BELOW'} ({((current_price/sma50-1)*100):+.2f}%)
Price vs SMA200:    {'ABOVE' if current_price > sma200 else 'BELOW'} ({((current_price/sma200-1)*100):+.2f}%)

{'='*80}
MOMENTUM INDICATORS
{'='*80}
"""
        
        # RSI Analysis
        rsi = df['RSI'].iloc[-1]
        rsi_signal = "OVERBOUGHT (>70)" if rsi > 70 else "OVERSOLD (<30)" if rsi < 30 else "NEUTRAL"
        
        report += f"""
RSI (14):           {rsi:.2f}
RSI Signal:         {rsi_signal}

"""
        
        # MACD Analysis
        macd = df['MACD'].iloc[-1]
        macd_signal = df['MACD_Signal'].iloc[-1]
        macd_hist = df['MACD_Hist'].iloc[-1]
        macd_trend = "BULLISH" if macd > macd_signal else "BEARISH"
        
        report += f"""
MACD:               {macd:.4f}
MACD Signal:        {macd_signal:.4f}
MACD Histogram:     {macd_hist:.4f}
MACD Signal:        {macd_trend} ({'BUY' if macd > macd_signal else 'SELL'})

"""
        
        # Stochastic
        stoch_k = df['Stoch_K'].iloc[-1]
        stoch_d = df['Stoch_D'].iloc[-1]
        stoch_signal = "OVERBOUGHT (>80)" if stoch_k > 80 else "OVERSOLD (<20)" if stoch_k < 20 else "NEUTRAL"
        
        report += f"""
Stochastic %K:      {stoch_k:.2f}
Stochastic %D:      {stoch_d:.2f}
Stochastic Signal:  {stoch_signal}

{'='*80}
VOLATILITY
{'='*80}
ATR (14):           ${df['ATR'].iloc[-1]:.2f}
BB Upper:           ${df['BB_Upper'].iloc[-1]:.2f}
BB Middle:          ${df['BB_Middle'].iloc[-1]:.2f}
BB Lower:           ${df['BB_Lower'].iloc[-1]:.2f}
BB Width:           ${df['BB_Upper'].iloc[-1] - df['BB_Lower'].iloc[-1]:.2f}

"""
        
        # Volatility metrics
        returns = df['Returns'].dropna()
        daily_vol = returns.std()
        annual_vol = daily_vol * np.sqrt(252)
        
        report += f"""
Daily Volatility:   {daily_vol*100:.2f}%
Annual Volatility:  {annual_vol*100:.2f}%

{'='*80}
SUPPORT & RESISTANCE LEVELS
{'='*80}
"""
        
        # Calculate pivot points
        high = df['High'].iloc[-1]
        low = df['Low'].iloc[-1]
        close = df['Close'].iloc[-1]
        
        pivot = (high + low + close) / 3
        r1 = 2 * pivot - low
        r2 = pivot + (high - low)
        r3 = high + 2 * (pivot - low)
        s1 = 2 * pivot - high
        s2 = pivot - (high - low)
        s3 = low - 2 * (high - pivot)
        
        report += f"""
Pivot Point:        ${pivot:.2f}

Resistance 3:       ${r3:.2f}
Resistance 2:       ${r2:.2f}
Resistance 1:       ${r1:.2f}

Support 1:          ${s1:.2f}
Support 2:          ${s2:.2f}
Support 3:          ${s3:.2f}

{'='*80}
TRADING SIGNALS
{'='*80}
"""
        
        # Generate trading signals
        signals = []
        
        if rsi < 30:
            signals.append("✓ RSI indicates OVERSOLD - Potential BUY signal")
        elif rsi > 70:
            signals.append("✗ RSI indicates OVERBOUGHT - Potential SELL signal")
        
        if macd > macd_signal and macd_hist > 0:
            signals.append("✓ MACD Bullish Crossover - BUY signal")
        elif macd < macd_signal and macd_hist < 0:
            signals.append("✗ MACD Bearish Crossover - SELL signal")
        
        if current_price > sma20 and sma20 > sma50:
            signals.append("✓ Price above SMA20 and SMA50 - Bullish trend")
        elif current_price < sma20 and sma20 < sma50:
            signals.append("✗ Price below SMA20 and SMA50 - Bearish trend")
        
        if stoch_k < 20:
            signals.append("✓ Stochastic OVERSOLD - Potential reversal UP")
        elif stoch_k > 80:
            signals.append("✗ Stochastic OVERBOUGHT - Potential reversal DOWN")
        
        if current_price <= df['BB_Lower'].iloc[-1]:
            signals.append("✓ Price at Lower Bollinger Band - Potential BUY")
        elif current_price >= df['BB_Upper'].iloc[-1]:
            signals.append("✗ Price at Upper Bollinger Band - Potential SELL")
        
        for signal in signals:
            report += f"{signal}\n"
        
        report += f"""
{'='*80}
RISK METRICS
{'='*80}
"""
        
        # Risk calculations
        total_return = ((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100
        max_price = df['Close'].max()
        max_drawdown = ((df['Close'].min() / max_price) - 1) * 100
        
        # Sharpe ratio (assuming 0% risk-free rate)
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else 0
        
        report += f"""
Total Return:       {total_return:+.2f}%
Max Drawdown:       {max_drawdown:.2f}%
Sharpe Ratio:       {sharpe_ratio:.2f}
Best Day:           {returns.max()*100:+.2f}%
Worst Day:          {returns.min()*100:+.2f}%

{'='*80}
RECOMMENDATION
{'='*80}
"""
        
        # Overall recommendation
        bullish_signals = sum([
            rsi < 30,
            macd > macd_signal,
            current_price > sma20,
            stoch_k < 20,
            current_price <= df['BB_Lower'].iloc[-1]
        ])
        
        bearish_signals = sum([
            rsi > 70,
            macd < macd_signal,
            current_price < sma20,
            stoch_k > 80,
            current_price >= df['BB_Upper'].iloc[-1]
        ])
        
        if bullish_signals > bearish_signals + 1:
            recommendation = "STRONG BUY"
        elif bullish_signals > bearish_signals:
            recommendation = "BUY"
        elif bearish_signals > bullish_signals + 1:
            recommendation = "STRONG SELL"
        elif bearish_signals > bullish_signals:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"
        
        report += f"""
Overall Rating:     {recommendation}
Bullish Signals:    {bullish_signals}/5
Bearish Signals:    {bearish_signals}/5

{'='*80}
DISCLAIMER
{'='*80}
This analysis is for informational purposes only and should not be considered
as financial advice. Always do your own research and consult with a qualified
financial advisor before making investment decisions.

{'='*80}
"""
        
        self.technical_text.insert(1.0, report)
    
    def calculate_portfolio(self):
        """Calculate portfolio P&L"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "Please analyze a stock first")
            return
        
        try:
            shares = float(self.shares_entry.get())
            buy_price = float(self.buy_price_entry.get())
            
            if shares <= 0 or buy_price <= 0:
                messagebox.showwarning("Warning", "Please enter valid positive numbers")
                return
            
            df = self.current_data['df']
            current_price = df['Close'].iloc[-1]
            
            # Calculate metrics
            total_cost = shares * buy_price
            current_value = shares * current_price
            pnl = current_value - total_cost
            pnl_pct = (pnl / total_cost) * 100
            
            # Daily P&L
            prev_price = df['Close'].iloc[-2]
            daily_pnl = shares * (current_price - prev_price)
            daily_pnl_pct = ((current_price / prev_price) - 1) * 100
            
            # Risk metrics
            position_size_pct = (current_value / 100000) * 100  # Assuming 100k portfolio
            
            # Generate report
            portfolio_report = f"""
{'='*80}
PORTFOLIO ANALYSIS
{'='*80}
Symbol:                 {self.current_symbol}
Shares Owned:           {shares:,.0f}

{'='*80}
POSITION DETAILS
{'='*80}
Buy Price:              ${buy_price:.2f}
Current Price:          ${current_price:.2f}
Price Change:           ${current_price - buy_price:+.2f} ({((current_price/buy_price-1)*100):+.2f}%)

{'='*80}
PORTFOLIO VALUE
{'='*80}
Total Cost Basis:       ${total_cost:,.2f}
Current Value:          ${current_value:,.2f}
Unrealized P&L:         ${pnl:+,.2f}
Return on Investment:   {pnl_pct:+.2f}%

{'='*80}
DAILY PERFORMANCE
{'='*80}
Yesterday's Close:      ${prev_price:.2f}
Today's Change:         ${current_price - prev_price:+.2f}
Daily P&L:              ${daily_pnl:+,.2f}
Daily Return:           {daily_pnl_pct:+.2f}%

{'='*80}
RISK ANALYSIS
{'='*80}
Position Size:          {position_size_pct:.2f}% of portfolio
Risk per Share:         ${current_price - buy_price:.2f}

Breakeven Price:        ${buy_price:.2f}
Current Distance:       {((current_price/buy_price-1)*100):+.2f}%

{'='*80}
PROFIT TARGETS
{'='*80}
"""
            
            # Calculate profit targets
            targets = [5, 10, 15, 20, 25, 50]
            for target_pct in targets:
                target_price = buy_price * (1 + target_pct/100)
                target_profit = shares * (target_price - buy_price)
                distance = ((target_price / current_price) - 1) * 100
                portfolio_report += f"+{target_pct}% Target:          ${target_price:.2f} (Profit: ${target_profit:,.2f}, Distance: {distance:+.2f}%)\n"
            
            portfolio_report += f"""
{'='*80}
STOP LOSS LEVELS
{'='*80}
"""
            
            # Calculate stop loss levels
            stop_levels = [5, 10, 15, 20]
            for stop_pct in stop_levels:
                stop_price = buy_price * (1 - stop_pct/100)
                stop_loss = shares * (buy_price - stop_price)
                distance = ((stop_price / current_price) - 1) * 100
                portfolio_report += f"-{stop_pct}% Stop:           ${stop_price:.2f} (Loss: -${stop_loss:,.2f}, Distance: {distance:+.2f}%)\n"
            
            portfolio_report += f"""
{'='*80}
RECOMMENDATION
{'='*80}
"""
            
            if pnl_pct > 20:
                portfolio_report += "Position is UP significantly. Consider taking partial profits.\n"
            elif pnl_pct > 10:
                portfolio_report += "Position is profitable. Consider trailing stop loss.\n"
            elif pnl_pct > 0:
                portfolio_report += "Position is slightly profitable. Monitor closely.\n"
            elif pnl_pct > -5:
                portfolio_report += "Position is near breakeven. Wait for clearer direction.\n"
            elif pnl_pct > -10:
                portfolio_report += "Position is DOWN. Review your thesis and consider stop loss.\n"
            else:
                portfolio_report += "Position is significantly DOWN. Consider cutting losses.\n"
            
            portfolio_report += f"""
{'='*80}
"""
            
            self.portfolio_text.delete(1.0, tk.END)
            self.portfolio_text.insert(1.0, portfolio_report)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def update_data_table(self):
        """Update data table"""
        if self.current_data is None:
            return
        
        df = self.current_data['df']
        
        # Clear existing data
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Insert new data (last 100 rows)
        display_df = df.tail(100).copy()
        display_df['Change_Pct'] = display_df['Close'].pct_change() * 100
        
        for idx, row in display_df.iterrows():
            date_str = row['Date'].strftime('%Y-%m-%d %H:%M')
            values = (
                date_str,
                f"${row['Open']:.2f}",
                f"${row['High']:.2f}",
                f"${row['Low']:.2f}",
                f"${row['Close']:.2f}",
                f"{row['Volume']:,.0f}",
                f"{row['Change_Pct']:+.2f}%"
            )
            
            # Color coding based on change
            tag = 'positive' if row['Change_Pct'] >= 0 else 'negative'
            self.data_tree.insert('', 0, values=values, tags=(tag,))
        
        # Configure tags
        self.data_tree.tag_configure('positive', foreground='#00ff88')
        self.data_tree.tag_configure('negative', foreground='#ff4444')
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        self.auto_refresh = self.auto_refresh_var.get()
        
        if self.auto_refresh:
            self.status_label.config(text="Auto-refresh enabled", foreground='#00ff88')
            threading.Thread(target=self.auto_refresh_loop, daemon=True).start()
        else:
            self.status_label.config(text="Auto-refresh disabled", foreground='#ffaa00')
    
    def auto_refresh_loop(self):
        """Auto-refresh loop"""
        while self.auto_refresh:
            time.sleep(self.refresh_interval)
            if self.auto_refresh:
                self.root.after(0, self.analyze)

def main():
    root = tk.Tk()
    app = FinancialAnalysisPro(root)
    root.mainloop()

if __name__ == "__main__":
    main()