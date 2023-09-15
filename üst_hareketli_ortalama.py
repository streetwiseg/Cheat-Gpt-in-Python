import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Yahoo Finance'ten veri çek
def fetch_data(stock, start_date, end_date):
    df = yf.download(stock, start=start_date, end=end_date)
    return df

def calculate_ema(df, window):
    df["EMA"] = df["Close"].ewm(span=window, adjust=False).mean()
    return df

# Veri çek
start_date = "2023-01-01"
end_date = "2023-09-14" 
stock = "THYAO.IS"
df = fetch_data(stock, start_date, end_date)

# EMA-10 hesapla
window = 10
df_with_ema = calculate_ema(df, window)

# EMA-10'u grafik üzerinde göster
plt.figure(figsize=(12,6))
df_with_ema["Close"].tail(15).plot(label='Kapanış Fiyatı', grid=True, title="THYAO Kapanış Fiyatı ve EMA-10")
df_with_ema["EMA"].tail(15).plot(label=f'EMA-{window}', grid=True)
plt.legend()
plt.show()
