import yfinance as yf
import pandas as pd
from ta.momentum import UltimateOscillator
import matplotlib.pyplot as plt

# Yahoo Finance'ten veri çek
def fetch_data(stock, start_date, end_date):
    df = yf.download(stock, start=start_date, end=end_date)
    return df

def calculate_uo(df):
    uo = UltimateOscillator(df["High"], df["Low"], df["Close"], window1=7, window2=14, window3=28, fillna=False)
    df["UO"] = uo.ultimate_oscillator()
    return df

# Veri çek
start_date = "2023-01-01"
end_date = "2023-09-01" 
stock = "THYAO.IS"
df = fetch_data(stock, start_date, end_date)

# UO hesapla
df_with_uo = calculate_uo(df)

# UO'yu grafik üzerinde göster
plt.figure(figsize=(12,6))
df_with_uo["UO"].tail(15).plot(grid=True, title="THYAO Nihai Osilatör (UO) Değerleri")
plt.axhline(50, color="gray", linestyle="--")  # 50 seviyesine bir çizgi çiz
plt.show()
