import yfinance as yf
import pandas as pd
from ta.momentum import StochasticOscillator
import matplotlib.pyplot as plt

# Yahoo Finance'ten veri çek
def fetch_data(stock, start_date, end_date):
    df = yf.download(stock, start=start_date, end=end_date)
    return df

def calculate_stochastic(df):
    stochastic = StochasticOscillator(df["High"], df["Low"], df["Close"], window=14, smooth_window=3, fillna=False)
    df["%K"] = stochastic.stoch()
    df["%D"] = stochastic.stoch_signal()
    return df

# Veri çek
start_date = "2023-01-01"
end_date = "2023-09-14" 
stock = "THYAO.IS"
df = fetch_data(stock, start_date, end_date)

# Stokastik Osilatör hesapla
df_with_stochastic = calculate_stochastic(df)

# Stokastik Osilatörü grafik üzerinde göster
plt.figure(figsize=(12,6))
df_with_stochastic["%K"].tail(15).plot(label='%K', grid=True, title="THYAO Stokastik Osilatör Değerleri")
df_with_stochastic["%D"].tail(15).plot(label='%D', grid=True)
plt.axhline(80, color="gray", linestyle="--")  # 80 seviyesine bir çizgi çiz
plt.axhline(20, color="gray", linestyle="--")  # 20 seviyesine bir çizgi çiz
plt.legend()
plt.show()
